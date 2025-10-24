from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from typing import Optional, cast

from .forms import (
    CustomUserCreationForm,
    EmailAwareAuthenticationForm,
    EmailVerificationForm,
    PasswordResetConfirmForm,
    PasswordResetRequestForm,
)
from .serializers import UserSerializer
from .models import User as UserModel

User = get_user_model()


class UserListView(generics.ListCreateAPIView):
    """List users (authenticated) or create a new user (open registration)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a user. Requires authentication."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class RegisterView(CreateView):
    """HTML endpoint for creating a user account and collecting email confirmation."""

    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('verify-email')

    def form_valid(self, form: forms.BaseModelForm) -> HttpResponse:
        user = cast(UserModel, form.save())
        self.request.session['pending_verification_user_id'] = user.pk
        self._send_confirmation_email(user)
        messages.success(self.request, 'We sent a confirmation code to your email. Enter it below to activate your account.')
        return redirect('verify-email')

    def _send_confirmation_email(self, user: UserModel) -> None:
        subject = 'Confirm your Contacts App email'
        message = (
            'Welcome to Contacts App!\n\n'
            f'Use the code {user.email_confirmation_code} to confirm your email address.\n'
            'Enter it on the confirmation page to finish setting up your account.'
        )
        send_mail(
            subject,
            message,
            getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com'),
            [user.email],
            fail_silently=True,
        )


class VerifyEmailView(FormView):
    """Allow users to enter the email confirmation code sent during registration."""

    template_name = 'users/verify_email.html'
    form_class = EmailVerificationForm
    success_url = reverse_lazy('contact-list')

    def dispatch(self, request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
        target_user = self._get_target_user()
        if not target_user:
            messages.info(request, 'No pending email confirmation found.')
            return redirect('home')
        self.target_user: UserModel = target_user
        return super().dispatch(request, *args, **kwargs)

    def _get_target_user(self) -> Optional[UserModel]:
        if self.request.user.is_authenticated:
            confirmed_user = cast(UserModel, self.request.user)
            if not confirmed_user.email_confirmed:
                return confirmed_user
        user_id = self.request.session.get('pending_verification_user_id')
        if user_id:
            return cast(Optional[UserModel], User.objects.filter(pk=user_id).first())
        return None

    def form_valid(self, form: EmailVerificationForm) -> HttpResponse:
        code = form.cleaned_data['code']
        if code != self.target_user.email_confirmation_code:
            form.add_error('code', 'That code does not match. Please try again.')
            return self.form_invalid(form)

        self.target_user.email_confirmed = True
        self.target_user.email_confirmation_code = ''
        self.target_user.save()
        self.request.session.pop('pending_verification_user_id', None)
        login(self.request, self.target_user)
        messages.success(self.request, 'Email confirmed! You are now signed in.')
        return super().form_valid(form)


class CustomLoginView(auth_views.LoginView):
    """Wrap Django's login view with email confirmation enforcement."""

    authentication_form = EmailAwareAuthenticationForm
    template_name = 'users/login.html'


class ForgotPasswordView(FormView):
    """Collect an email and send a reset code when possible."""

    template_name = 'users/forgot_password.html'
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy('reset-password-confirm')

    def form_valid(self, form: PasswordResetRequestForm) -> HttpResponse:
        email = form.cleaned_data['email']
        user = cast(Optional[UserModel], User.objects.filter(email__iexact=email).first())
        if user:
            user.generate_password_reset_code()
            user.save(update_fields=['password_reset_code', 'password_reset_requested_at'])
            self.request.session['password_reset_user_id'] = user.pk
            self._send_reset_email(user)
        messages.success(self.request, 'If an account with that email exists, we sent a reset code.')
        return redirect('reset-password-confirm')

    def _send_reset_email(self, user: UserModel) -> None:
        subject = 'Reset your Contacts App password'
        message = (
            'We received a request to reset your Contacts App password.\n\n'
            f'Use the code {user.password_reset_code} to choose a new password.\n'
            'If you did not make this request, you can ignore this email.'
        )
        send_mail(
            subject,
            message,
            getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com'),
            [user.email],
            fail_silently=True,
        )


class ResetPasswordConfirmView(FormView):
    """Allow users to confirm their reset code and choose a new password."""

    template_name = 'users/reset_password_confirm.html'
    form_class = PasswordResetConfirmForm
    success_url = reverse_lazy('contact-list')

    def dispatch(self, request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
        reset_user = self._get_reset_user()
        if not reset_user:
            messages.info(request, 'Start by requesting a password reset code.')
            return redirect('forgot-password')
        self.reset_user: UserModel = reset_user
        return super().dispatch(request, *args, **kwargs)

    def _get_reset_user(self) -> Optional[UserModel]:
        user_id = self.request.session.get('password_reset_user_id')
        if user_id:
            return cast(Optional[UserModel], User.objects.filter(pk=user_id).first())
        return None

    def get_form_kwargs(self) -> dict[str, object]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.reset_user
        return kwargs

    def form_valid(self, form: PasswordResetConfirmForm) -> HttpResponse:
        new_password = form.cleaned_data['new_password1']
        self.reset_user.set_password(new_password)
        self.reset_user.password_reset_code = ''
        self.reset_user.password_reset_requested_at = None
        self.reset_user.save()
        self.request.session.pop('password_reset_user_id', None)
        login(self.request, self.reset_user)
        messages.success(self.request, 'Password updated successfully. You are now signed in.')
        return super().form_valid(form)