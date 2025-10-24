from django_filters import rest_framework as filters
from .models import Contact

class ContactFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    phone = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone']