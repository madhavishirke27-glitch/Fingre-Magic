"""
FaceStyle AI - Django Database Models
Compatible with SQLite and MySQL databases.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json


class UserProfile(models.Model):
    """Extended user profile information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, help_text="Short bio or personal hair goals")
    preferred_hair_length = models.CharField(
        max_length=20,
        choices=[('All', 'Any Length'), ('Short', 'Short'), ('Medium', 'Medium'), ('Long', 'Long')],
        default='All'
    )
    preferred_hair_type = models.CharField(
        max_length=20,
        choices=[('All', 'Any Texture'), ('Straight', 'Straight'), ('Wavy', 'Wavy'), ('Curly', 'Curly')],
        default='All'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()


class Hairstyle(models.Model):
    """Hairstyle catalog item with metadata and face shape affinities."""
    LENGTH_CHOICES = [
        ('Short', 'Short Hairstyles'),
        ('Medium', 'Medium Hairstyles'),
        ('Long', 'Long Hairstyles'),
    ]
    TYPE_CHOICES = [
        ('Straight', 'Straight Hair'),
        ('Wavy', 'Wavy Hair'),
        ('Curly', 'Curly Hair'),
    ]
    CATEGORY_CHOICES = [
        ('Modern', 'Modern Hairstyles'),
        ('Traditional', 'Traditional Hairstyles'),
        ('Casual', 'Casual Everyday'),
        ('Formal', 'Formal & Professional'),
    ]
    GENDER_CHOICES = [
        ('Female', 'Women'),
        ('Male', 'Men'),
        ('Unisex', 'Unisex (All)'),
    ]

    name = models.CharField(max_length=150, unique=True, help_text="E.g., Textured Layered Bob, Classic Pompadour")
    description = models.TextField(help_text="Detailed description of the cut, silhouette, and maintenance.")
    styling_tips = models.TextField(blank=True, help_text="Step-by-step styling suggestions and recommended hair products.")
    image = models.ImageField(upload_to='hairstyles/', help_text="Hairstyle visual representation")
    
    # Comma-separated face shapes, e.g., 'Oval, Heart, Square'
    face_shapes = models.CharField(
        max_length=200,
        help_text="Compatible face shapes separated by comma (Oval, Round, Square, Heart, Diamond, Oblong)"
    )
    hair_length = models.CharField(max_length=20, choices=LENGTH_CHOICES, default='Medium')
    hair_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Wavy')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Modern')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Unisex')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Hairstyle'
        verbose_name_plural = 'Hairstyles'

    def __str__(self):
        return f"{self.name} ({self.gender} - {self.hair_length})"

    def get_compatible_face_shapes(self):
        """Returns a list of clean face shape names."""
        return [shape.strip() for shape in self.face_shapes.split(',') if shape.strip()]

    def is_compatible_with(self, shape_name):
        return shape_name.lower() in [s.lower() for s in self.get_compatible_face_shapes()]


class FaceAnalysis(models.Model):
    """Face shape analysis record, with privacy-first optional photo persistence."""
    FACE_SHAPE_CHOICES = [
        ('Oval', 'Oval Face'),
        ('Round', 'Round Face'),
        ('Square', 'Square Face'),
        ('Heart', 'Heart Face'),
        ('Diamond', 'Diamond Face'),
        ('Oblong', 'Oblong Face'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='face_analyses', null=True, blank=True)
    session_key = models.CharField(max_length=100, blank=True, null=True, help_text="Session key for guest visitors")
    
    detected_face_shape = models.CharField(max_length=30, choices=FACE_SHAPE_CHOICES)
    confidence = models.FloatField(default=85.0, help_text="Calibrated estimation confidence percentage")
    
    # Key facial proportions
    length_width_ratio = models.FloatField(default=1.35)
    forehead_width = models.FloatField(default=0.0)
    cheekbone_width = models.FloatField(default=0.0)
    jaw_width = models.FloatField(default=0.0)
    
    # Privacy options: user can choose whether to retain original photo
    retain_photo = models.BooleanField(default=False, help_text="Did the user consent to save the photo in history?")
    original_image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    annotated_image = models.ImageField(upload_to='annotated/', null=True, blank=True)
    
    measurements_json = models.TextField(blank=True, default="{}", help_text="Detailed JSON dump of all ratios and scores")
    observations_json = models.TextField(blank=True, default="[]", help_text="List of AI proportion observations")
    
    analysis_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-analysis_date']
        verbose_name = 'Face Analysis Record'
        verbose_name_plural = 'Face Analysis Records'

    def __str__(self):
        user_label = self.user.username if self.user else "Guest"
        return f"{user_label} - {self.detected_face_shape} ({self.analysis_date.strftime('%Y-%m-%d %H:%M')})"

    def get_measurements(self):
        try:
            return json.loads(self.measurements_json)
        except Exception:
            return {}

    def get_observations(self):
        try:
            return json.loads(self.observations_json)
        except Exception:
            return []


class FavouriteHairstyle(models.Model):
    """User's bookmarked favorite hairstyles."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    hairstyle = models.ForeignKey(Hairstyle, on_delete=models.CASCADE, related_name='favourited_by')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']
        unique_together = ('user', 'hairstyle')
        verbose_name = 'Favourite Hairstyle'
        verbose_name_plural = 'Favourite Hairstyles'

    def __str__(self):
        return f"{self.user.username} saved {self.hairstyle.name}"
