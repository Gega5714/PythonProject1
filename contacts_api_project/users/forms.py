from typing import Any, Optional, cast

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    """Model-backed form used for HTML user registration."""

    phone = forms.CharField(
        max_length=20,
        required=False,
        help_text="Optional. Include country code if outside your region.",
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'phone',)

    def __init__(self, *args: object, **kwargs: object):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        user.phone = self.cleaned_data.get('phone', '')
        user.email_confirmed = False
        user.generate_confirmation_code()
        if commit:
            user.save()
        return user


class EmailVerificationForm(forms.Form):
    """Collect the code sent to the user's email for confirmation."""

    code = forms.CharField(max_length=6, strip=True)


class EmailAwareAuthenticationForm(AuthenticationForm):
    """Prevent login for users who have not confirmed their email."""

    def confirm_login_allowed(self, user: AbstractBaseUser) -> None:
        super().confirm_login_allowed(user)
        if not getattr(user, 'email_confirmed', True):
            raise forms.ValidationError(
                "Please confirm your email address before logging in.",
                code='email_not_confirmed',
            )


class PasswordResetRequestForm(forms.Form):
    """Collect the email address for initiating a password reset."""

    email = forms.EmailField(label='Email address')


class PasswordResetConfirmForm(forms.Form):
    """Allow the user to submit their reset code and a new password."""

    code = forms.CharField(max_length=6, strip=True, label='Reset code')
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput,
        strip=False,
    )
    new_password2 = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput,
        strip=False,
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        kwargs_dict = dict(kwargs)
        user_value = kwargs_dict.pop('user', None)
        self.user = cast(Optional[AbstractBaseUser], user_value)
        super().__init__(*args, **kwargs_dict)  # type: ignore[arg-type]

    def clean_code(self) -> str:
        code = self.cleaned_data['code']
        if not self.user:
            raise forms.ValidationError('No active password reset session was found.')
        if getattr(self.user, 'password_reset_code', '') != code:
            raise forms.ValidationError('That code does not match our records. Please try again.')
        return code

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The two password fields must match.')
        return cleaned_data
