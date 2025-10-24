from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    """Simple form for CRUD operations on contacts via HTML views."""

    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'address')
