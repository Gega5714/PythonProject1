import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom user model extending Django's base user with phone and email confirmation."""

    phone = models.CharField(max_length=20, blank=True)
    email_confirmed = models.BooleanField(default=False)
    email_confirmation_code = models.CharField(max_length=6, blank=True)
    email_confirmation_sent_at = models.DateTimeField(null=True, blank=True)
    password_reset_code = models.CharField(max_length=6, blank=True)
    password_reset_requested_at = models.DateTimeField(null=True, blank=True)

    def generate_confirmation_code(self) -> str:
        """Create and store a new six-digit confirmation code."""

        code = ''.join(secrets.choice('0123456789') for _ in range(6))
        self.email_confirmation_code = code
        self.email_confirmation_sent_at = timezone.now()
        return code

    def generate_password_reset_code(self) -> str:
        """Create and store a reset code used during the password reset flow."""

        code = ''.join(secrets.choice('0123456789') for _ in range(6))
        self.password_reset_code = code
        self.password_reset_requested_at = timezone.now()
        return code
