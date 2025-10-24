from rest_framework import viewsets, permissions
from rest_framework import filters
from .models import Contact
from .serializers import ContactSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email', 'phone']

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)