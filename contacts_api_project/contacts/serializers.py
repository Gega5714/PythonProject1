from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'user', 'name', 'email', 'phone', 'address']  # Add any other fields as necessary

class ContactUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'address']  # Fields that can be updated, excluding user field
        read_only_fields = ['user']  # Ensure user field is read-only during updates