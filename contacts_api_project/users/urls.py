from django.urls import path

from .views import (
    ForgotPasswordView,
    RegisterView,
    ResetPasswordConfirmView,
    UserDetailView,
    UserListView,
    VerifyEmailView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyEmailView.as_view(), name='verify-email'),
    path('password/forgot/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('password/reset/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),
    path('api/', UserListView.as_view(), name='user-list'),
    path('api/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]