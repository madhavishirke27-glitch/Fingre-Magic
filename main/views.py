"""
FaceStyle AI - Views and Application Controller Logic
"""
import os
import json
import base64
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.core.files.base import ContentFile
from django.conf import settings
from django.db.models import Q

from .models import UserProfile, Hairstyle, FaceAnalysis, FavouriteHairstyle
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    ImageUploadForm,
    HairstyleFilterForm,
    UserProfileForm
)
from ai_engine.face_detection import detect_face_and_analyze
from ai_engine.measurements import FACE_SHAPE_DETAILS
from ai_engine.recommendation import get_face_shape_details, get_styling_principles, get_recommendations


# ==============================================================================
# 1. PUBLIC LANDING & ABOUT VIEWS
# ==============================================================================

def home_view(request):
    """Modern landing page highlighting AI face analysis and trending hairstyles."""
    # Fetch sample featured hairstyles
    featured_hairstyles = Hairstyle.objects.all()[:6]
    face_shapes = [
        {'name': 'Oval', 'title': 'Oval Face', 'desc': 'Universally balanced with soft contours.', 'icon': 'fa-egg'},
        {'name': 'Round', 'title': 'Round Face', 'desc': 'Soft cheeks with symmetrical width and height.', 'icon': 'fa-circle'},
        {'name': 'Square', 'title': 'Square Face', 'desc': 'Sharp, angular jawline with proportional forehead.', 'icon': 'fa-square'},
        {'name': 'Heart', 'title': 'Heart Face', 'desc': 'Broad forehead tapering to a delicate chin.', 'icon': 'fa-heart'},
        {'name': 'Diamond', 'title': 'Diamond Face', 'desc': 'Dramatic high cheekbones with sculpted contours.', 'icon': 'fa-gem'},
        {'name': 'Oblong', 'title': 'Oblong Face', 'desc': 'Elongated silhouette with balanced vertical lines.', 'icon': 'fa-rectangle-vertical'},
    ]
    return render(request, 'home.html', {
        'featured_hairstyles': featured_hairstyles,
        'face_shapes': face_shapes,
    })


def about_view(request):
    """Detailed architectural explanation of FaceStyle AI, facial landmark ratios, and ethics."""
    return render(request, 'about.html', {
        'face_shape_details': FACE_SHAPE_DETAILS,
    })


# ==============================================================================
# 2. USER AUTHENTICATION VIEWS
# ==============================================================================

def register_view(request):
    """Handles new user registration with full validation and instant session login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # UserProfile created via post_save signal
            login(request, user)
            messages.success(request, f"Welcome to FaceStyle AI, {user.first_name or user.username}! Your account is ready.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors in the registration form below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Login supporting both username and email credentials."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email'].strip()
            password = form.cleaned_data['password']

            # Lookup by email if entered as email
            if '@' in username_or_email:
                try:
                    user_obj = User.objects.get(email__iexact=username_or_email)
                    username = user_obj.username
                except User.DoesNotExist:
                    username = None
            else:
                username = username_or_email

            user = None
            if username:
                user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username/email or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Logs out user safely and clears session."""
    logout(request)
    messages.info(request, "You have been logged out securely. See you again!")
    return redirect('home')


# ==============================================================================
# 3. USER DASHBOARD & PROFILE
# ==============================================================================

@login_required
def dashboard_view(request):
    """Centralized user dashboard showing metrics, recent analyses, and style recommendations."""
    analyses = FaceAnalysis.objects.filter(user=request.user).order_by('-analysis_date')
    recent_analyses = analyses[:4]
    latest_analysis = analyses.first()

    # Get user's favorites
    user_favourites = FavouriteHairstyle.objects.filter(user=request.user).select_related('hairstyle')
    fav_count = user_favourites.count()

    # Recommendations based on latest detected shape (or default to Oval if none yet)
    active_shape = latest_analysis.detected_face_shape if latest_analysis else 'Oval'
    recommended_hairstyles = Hairstyle.objects.filter(face_shapes__icontains=active_shape)[:6]

    fav_ids = set(user_favourites.values_list('hairstyle_id', flat=True))

    return render(request, 'dashboard.html', {
        'total_analyses': analyses.count(),
        'latest_analysis': latest_analysis,
        'recent_analyses': recent_analyses,
        'fav_count': fav_count,
        'active_shape': active_shape,
        'recommended_hairstyles': recommended_hairstyles,
        'fav_ids': fav_ids,
    })


@login_required
def profile_view(request):
    """User profile management for hair preferences and personal details."""
    profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Update User basic fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            form.save()
            messages.success(request, "Your profile and styling preferences have been updated.")
            return redirect('profile')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = UserProfileForm(instance=profile, initial=initial_data)

    return render(request, 'profile.html', {'form': form})


# ==============================================================================
# 4. AI FACE ANALYSIS ENGINE CONTROLLER
# ==============================================================================

def analyze_face_view(request):
    """
    Core AI face detection and analysis controller.
    Accepts photo uploads or live webcam captures, validates geometry,
    extracts MediaPipe landmarks, and persists privacy-configured results.
    """
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data.get('image_file')
            webcam_data = form.cleaned_data.get('webcam_image_data')
            retain_photo = form.cleaned_data.get('retain_photo', False)

            img_bgr = None
            orig_filename = None
            orig_content_file = None

            # Process 1: Live Webcam Capture
            if webcam_data and 'base64,' in webcam_data:
                try:
                    format_header, imgstr = webcam_data.split(';base64,')
                    img_bytes = base64.b64decode(imgstr)
                    nparr = np.frombuffer(img_bytes, np.uint8)
                    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    orig_filename = f"capture_{request.user.id or 'guest'}.jpg"
                    orig_content_file = ContentFile(img_bytes, name=orig_filename)
                except Exception as e:
                    messages.error(request, f"Error processing webcam snapshot: {str(e)}")
                    return render(request, 'upload.html', {'form': form})

            # Process 2: File Upload
            elif image_file:
                try:
                    file_bytes = image_file.read()
                    nparr = np.frombuffer(file_bytes, np.uint8)
                    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    orig_filename = image_file.name
                    orig_content_file = ContentFile(file_bytes, name=orig_filename)
                except Exception as e:
                    messages.error(request, f"Error reading uploaded image file: {str(e)}")
                    return render(request, 'upload.html', {'form': form})

            # Run MediaPipe AI Landmark & Face Analysis
            result = detect_face_and_analyze(img_bgr, save_annotated=True)

            if not result['success']:
                messages.error(request, result['error_message'])
                return render(request, 'upload.html', {'form': form})

            # Unpack results
            classification = result['classification']
            measurements = result['measurements']
            face_shape = classification['face_shape']
            confidence = classification['confidence']
            observations = classification['observations']

            # Create FaceAnalysis record
            analysis_record = FaceAnalysis(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key or 'guest',
                detected_face_shape=face_shape,
                confidence=confidence,
                length_width_ratio=measurements['length_to_width_ratio'],
                forehead_width=measurements['forehead_width'],
                cheekbone_width=measurements['cheekbone_width'],
                jaw_width=measurements['jaw_width'],
                retain_photo=retain_photo,
                measurements_json=json.dumps(measurements),
                observations_json=json.dumps(observations)
            )

            # Privacy setting: save original photo only if consented
            if retain_photo and orig_content_file:
                analysis_record.original_image.save(orig_filename, orig_content_file, save=False)

            # Save annotated landmark image if available
            if result.get('annotated_image_filename'):
                analysis_record.annotated_image = f"annotated/{result['annotated_image_filename']}"

            analysis_record.save()

            messages.success(request, f"AI Analysis Complete! Your face shape is estimated as {face_shape}.")
            return redirect('result', analysis_id=analysis_record.id)
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})


def result_view(request, analysis_id):
    """
    Renders detailed face shape analysis results, geometric metrics,
    facial landmark visualization, and matched hairstyle recommendations.
    """
    analysis = get_object_or_404(FaceAnalysis, id=analysis_id)

    # Permission check: allow owner or guest session
    if analysis.user and request.user.is_authenticated and analysis.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view this analysis record.")

    face_shape = analysis.detected_face_shape
    shape_details = get_face_shape_details(face_shape)
    styling_principles = get_styling_principles(face_shape)
    measurements = analysis.get_measurements()
    observations = analysis.get_observations()

    # Query matching hairstyles
    matched_hairstyles = Hairstyle.objects.filter(face_shapes__icontains=face_shape)

    # Hair length sub-categories for quick tabs
    short_styles = matched_hairstyles.filter(hair_length='Short')
    medium_styles = matched_hairstyles.filter(hair_length='Medium')
    long_styles = matched_hairstyles.filter(hair_length='Long')

    # User favorite IDs
    fav_ids = set()
    if request.user.is_authenticated:
        fav_ids = set(FavouriteHairstyle.objects.filter(user=request.user).values_list('hairstyle_id', flat=True))

    return render(request, 'result.html', {
        'analysis': analysis,
        'face_shape': face_shape,
        'shape_details': shape_details,
        'styling_principles': styling_principles,
        'measurements': measurements,
        'observations': observations,
        'matched_hairstyles': matched_hairstyles,
        'short_styles': short_styles,
        'medium_styles': medium_styles,
        'long_styles': long_styles,
        'fav_ids': fav_ids,
    })


# ==============================================================================
# 5. HAIRSTYLES CATALOG & FILTERING
# ==============================================================================

def hairstyles_view(request):
    """
    Full hairstyle catalog with multi-dimensional filtering
    (length, texture, category, face shape, and search query).
    """
    form = HairstyleFilterForm(request.GET or None)
    hairstyles = Hairstyle.objects.all()

    active_shape = request.GET.get('face_shape', '')
    active_length = request.GET.get('hair_length', '')
    active_type = request.GET.get('hair_type', '')
    active_category = request.GET.get('category', '')
    active_gender = request.GET.get('gender', '')
    search_query = request.GET.get('search', '').strip()

    if search_query:
        hairstyles = hairstyles.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(styling_tips__icontains=search_query)
        )

    if active_shape:
        hairstyles = hairstyles.filter(face_shapes__icontains=active_shape)

    if active_length:
        hairstyles = hairstyles.filter(hair_length=active_length)

    if active_type:
        hairstyles = hairstyles.filter(hair_type=active_type)

    if active_category:
        hairstyles = hairstyles.filter(category=active_category)

    if active_gender:
        hairstyles = hairstyles.filter(Q(gender=active_gender) | Q(gender='Unisex'))

    fav_ids = set()
    if request.user.is_authenticated:
        fav_ids = set(FavouriteHairstyle.objects.filter(user=request.user).values_list('hairstyle_id', flat=True))

    return render(request, 'hairstyles.html', {
        'hairstyles': hairstyles,
        'form': form,
        'total_count': hairstyles.count(),
        'fav_ids': fav_ids,
        'active_shape': active_shape,
    })


def hairstyle_detail_view(request, hairstyle_id):
    """Detailed view for a specific hairstyle with styling tips and compatible shapes."""
    hairstyle = get_object_or_404(Hairstyle, id=hairstyle_id)
    is_favourite = False
    if request.user.is_authenticated:
        is_favourite = FavouriteHairstyle.objects.filter(user=request.user, hairstyle=hairstyle).exists()

    # Similar hairstyles in same category or length
    similar_styles = Hairstyle.objects.filter(
        hair_length=hairstyle.hair_length
    ).exclude(id=hairstyle.id)[:4]

    return render(request, 'hairstyle_detail.html', {
        'hairstyle': hairstyle,
        'is_favourite': is_favourite,
        'similar_styles': similar_styles,
    })


# ==============================================================================
# 6. FAVOURITES MANAGEMENT
# ==============================================================================

@login_required
def toggle_favourite_view(request, hairstyle_id):
    """Toggles hairstyle bookmark in user favourites (supports both AJAX and POST)."""
    hairstyle = get_object_or_404(Hairstyle, id=hairstyle_id)
    fav_obj = FavouriteHairstyle.objects.filter(user=request.user, hairstyle=hairstyle).first()

    if fav_obj:
        fav_obj.delete()
        is_fav = False
        message = f"Removed '{hairstyle.name}' from your favourites."
    else:
        FavouriteHairstyle.objects.create(user=request.user, hairstyle=hairstyle)
        is_fav = True
        message = f"Saved '{hairstyle.name}' to your favourites!"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({
            'status': 'success',
            'is_favourite': is_fav,
            'message': message,
            'hairstyle_id': hairstyle_id
        })

    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'hairstyles'))


@login_required
def favourites_view(request):
    """Displays user's saved hairstyles collection."""
    favourites = FavouriteHairstyle.objects.filter(user=request.user).select_related('hairstyle')
    return render(request, 'favourites.html', {
        'favourites': favourites,
        'total_saved': favourites.count(),
    })


# ==============================================================================
# 7. ANALYSIS HISTORY & PRIVACY MANAGEMENT
# ==============================================================================

@login_required
def history_view(request):
    """Displays chronological history of past face shape analyses for the logged-in user."""
    history_items = FaceAnalysis.objects.filter(user=request.user).order_by('-analysis_date')
    return render(request, 'history.html', {
        'history_items': history_items,
        'total_history': history_items.count(),
    })


@login_required
def delete_history_view(request, analysis_id):
    """Deletes an analysis record and securely wipes associated image files from disk."""
    analysis = get_object_or_404(FaceAnalysis, id=analysis_id, user=request.user)

    if request.method == 'POST':
        # Remove uploaded and annotated images from disk
        if analysis.original_image and os.path.isfile(analysis.original_image.path):
            try:
                os.remove(analysis.original_image.path)
            except Exception:
                pass

        if analysis.annotated_image and os.path.isfile(analysis.annotated_image.path):
            try:
                os.remove(analysis.annotated_image.path)
            except Exception:
                pass

        analysis.delete()
        messages.success(request, "Analysis record and associated media permanently deleted.")
        return redirect('history')

    return render(request, 'confirm_delete.html', {
        'analysis': analysis,
        'title': 'Delete Analysis Record',
        'cancel_url': 'history'
    })


@login_required
def clear_all_history_view(request):
    """Wipes all analysis history and corresponding images for the logged in user."""
    if request.method == 'POST':
        analyses = FaceAnalysis.objects.filter(user=request.user)
        count = analyses.count()
        for a in analyses:
            if a.original_image and os.path.isfile(a.original_image.path):
                try:
                    os.remove(a.original_image.path)
                except Exception:
                    pass
            if a.annotated_image and os.path.isfile(a.annotated_image.path):
                try:
                    os.remove(a.annotated_image.path)
                except Exception:
                    pass
        analyses.delete()
        messages.success(request, f"Cleared {count} analysis records and associated media permanently.")
        return redirect('history')

    return redirect('history')
