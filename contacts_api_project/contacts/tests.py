from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Contact
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.contact = Contact.objects.create(
            user=self.user,
            name='John Doe',
            email='john@example.com',
            phone='1234567890'
        )

    def test_create_contact(self):
        url = reverse('contact-list')
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '0987654321'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 2)

    def test_update_contact(self):
        url = reverse('contact-detail', args=[self.contact.id])
        data = {
            'name': 'John Smith',
            'email': 'johnsmith@example.com',
            'phone': '1234567890'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, 'John Smith')

    def test_delete_contact(self):
        url = reverse('contact-detail', args=[self.contact.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0)

    def test_list_contacts(self):
        url = reverse('contact-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_contacts(self):
        url = reverse('contact-list') + '?search=John'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)