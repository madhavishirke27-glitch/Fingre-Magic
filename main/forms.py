"""
FaceStyle AI - Django Forms with Strict Validation and Privacy Controls
"""
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, Hairstyle
import base64
import io
from PIL import Image


class UserRegistrationForm(forms.ModelForm):
    """User registration form with strict password confirmation and validation."""
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'})
    )
    username = forms.CharField(
        max_length=40,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a unique username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create strong password'}),
        min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        cpwd = cleaned_data.get('confirm_password')

        if pwd and cpwd and pwd != cpwd:
            self.add_error('confirm_password', "Passwords do not match. Please verify and re-enter.")
        return cleaned_data


class UserLoginForm(forms.Form):
    """User login supporting either username or email address."""
    username_or_email = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or email address'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )


class ImageUploadForm(forms.Form):
    """
    Dual-source upload form:
    1. Direct file upload (JPG/PNG <= 10MB)
    2. Base64 live webcam snapshot capture
    """
    image_file = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control d-none',
            'id': 'id_image_file',
            'accept': 'image/jpeg,image/png,image/jpg'
        })
    )
    webcam_image_data = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'id_webcam_image_data'})
    )
    retain_photo = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_retain_photo'}),
        label="Save photo thumbnail in my private history (optional, can be deleted anytime)"
    )

    def clean(self):
        cleaned_data = super().clean()
        image_file = cleaned_data.get('image_file')
        webcam_data = cleaned_data.get('webcam_image_data')

        if not image_file and not webcam_data:
            raise ValidationError("Please either upload a photo from your device or capture one using your camera.")

        # Check uploaded file size & format
        if image_file:
            if image_file.size > 10 * 1024 * 1024:
                raise ValidationError("Image file size exceeds maximum limit of 10 MB.")
            ext = image_file.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                raise ValidationError("Invalid format. Only JPG, JPEG, and PNG images are supported.")

        return cleaned_data


class HairstyleFilterForm(forms.Form):
    """Multi-criteria filtering for hairstyle discovery."""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by hairstyle name or feature...'})
    )
    face_shape = forms.ChoiceField(
        required=False,
        choices=[('', 'All Face Shapes')] + [
            ('Oval', 'Oval Face'),
            ('Round', 'Round Face'),
            ('Square', 'Square Face'),
            ('Heart', 'Heart Face'),
            ('Diamond', 'Diamond Face'),
            ('Oblong', 'Oblong Face'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    hair_length = forms.ChoiceField(
        required=False,
        choices=[('', 'All Lengths')] + Hairstyle.LENGTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    hair_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Textures')] + Hairstyle.TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + Hairstyle.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    gender = forms.ChoiceField(
        required=False,
        choices=[('', 'All Collections (Men, Women, Unisex)')] + Hairstyle.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class UserProfileForm(forms.ModelForm):
    """Allows user to update personal preferences and bio."""
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['preferred_hair_length', 'preferred_hair_type', 'bio']
        widgets = {
            'preferred_hair_length': forms.Select(attrs={'class': 'form-select'}),
            'preferred_hair_type': forms.Select(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your styling goals...'}),
        }
