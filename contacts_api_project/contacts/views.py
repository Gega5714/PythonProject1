from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets, permissions
from rest_framework import filters

from .forms import ContactForm
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


class ContactListView(LoginRequiredMixin, ListView):
    """HTML view showing the authenticated user's contacts."""

    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user).order_by('name')


class ContactCreateView(LoginRequiredMixin, CreateView):
    """Create a new contact bound to the current user."""

    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'
    success_url = reverse_lazy('contact-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    """Edit an existing contact owned by the current user."""

    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'
    success_url = reverse_lazy('contact-list')

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    """Delete one of the user's contacts after confirmation."""

    model = Contact
    template_name = 'contacts/contact_confirm_delete.html'
    success_url = reverse_lazy('contact-list')

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)