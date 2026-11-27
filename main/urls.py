"""
FaceStyle AI - URL Routing Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    # Core Public Pages
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    
    # Authentication Pages
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User Dashboard & Profile
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # AI Face Analysis
    path('analyze/', views.analyze_face_view, name='analyze'),
    path('result/<int:analysis_id>/', views.result_view, name='result'),
    
    # Hairstyle Recommendations & Catalog
    path('hairstyles/', views.hairstyles_view, name='hairstyles'),
    path('hairstyles/<int:hairstyle_id>/', views.hairstyle_detail_view, name='hairstyle_detail'),
    path('hairstyles/<int:hairstyle_id>/favourite/', views.toggle_favourite_view, name='toggle_favourite'),
    
    # Favourites & History
    path('favourites/', views.favourites_view, name='favourites'),
    path('history/', views.history_view, name='history'),
    path('history/<int:analysis_id>/delete/', views.delete_history_view, name='delete_history'),
    path('history/clear/', views.clear_all_history_view, name='clear_all_history'),
]
