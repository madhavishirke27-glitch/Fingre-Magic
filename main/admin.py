"""
FaceStyle AI - Django Administration Dashboard
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, Hairstyle, FaceAnalysis, FavouriteHairstyle


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_hair_length', 'preferred_hair_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('preferred_hair_length', 'preferred_hair_type')


@admin.register(Hairstyle)
class HairstyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'hair_length', 'hair_type', 'category', 'face_shapes_badge', 'image_preview')
    list_filter = ('gender', 'hair_length', 'hair_type', 'category')
    search_fields = ('name', 'description', 'face_shapes', 'styling_tips')
    list_per_page = 20

    def face_shapes_badge(self, obj):
        shapes = obj.get_compatible_face_shapes()
        badges = [f'<span style="background:#5A189A;color:#fff;padding:2px 7px;border-radius:10px;font-size:11px;margin:2px;display:inline-block;">{s}</span>' for s in shapes]
        return format_html("".join(badges))
    face_shapes_badge.short_description = 'Compatible Face Shapes'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:8px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'


@admin.register(FaceAnalysis)
class FaceAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_display', 'detected_face_shape', 'confidence_display', 'length_width_ratio', 'analysis_date', 'annotated_preview')
    list_filter = ('detected_face_shape', 'analysis_date', 'retain_photo')
    search_fields = ('user__username', 'user__email', 'detected_face_shape')
    readonly_fields = ('analysis_date', 'measurements_json', 'observations_json')
    list_per_page = 25

    def user_display(self, obj):
        return obj.user.username if obj.user else "Guest Visitor"
    user_display.short_description = 'User'

    def confidence_display(self, obj):
        return f"{obj.confidence}%"
    confidence_display.short_description = 'Confidence'

    def annotated_preview(self, obj):
        if obj.annotated_image:
            return format_html('<img src="{}" style="width:55px;height:55px;object-fit:cover;border-radius:8px;" />', obj.annotated_image.url)
        elif obj.original_image:
            return format_html('<img src="{}" style="width:55px;height:55px;object-fit:cover;border-radius:8px;" />', obj.original_image.url)
        return "No Photo"
    annotated_preview.short_description = 'Analyzed Photo'


@admin.register(FavouriteHairstyle)
class FavouriteHairstyleAdmin(admin.ModelAdmin):
    list_display = ('user', 'hairstyle', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('user__username', 'hairstyle__name')
