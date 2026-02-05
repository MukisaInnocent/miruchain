"""
URL configuration for Users app.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-referral-code', views.verify_referral_code, name='verify_referral_code'),
    path('forgot-password', views.request_password_reset, name='forgot_password'),
    
    # User Profile
    path('me', views.UserProfileView.as_view(), name='profile'),
    path('me/dashboard', views.UserDashboardView.as_view(), name='dashboard'),
    path('me/change-password', views.ChangePasswordView.as_view(), name='change_password'),
    path('me/referral-link', views.get_referral_link, name='referral_link'),
]
