from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
	ContactCreateView,
	ContactDeleteView,
	ContactListView,
	ContactUpdateView,
	ContactViewSet,
)

router = DefaultRouter()
# API endpoints now live under /contacts/api/.
router.register(r'', ContactViewSet, basename='contact-api')

urlpatterns = [
	path('', ContactListView.as_view(), name='contact-list'),
	path('create/', ContactCreateView.as_view(), name='contact-create'),
	path('<int:pk>/edit/', ContactUpdateView.as_view(), name='contact-edit'),
	path('<int:pk>/delete/', ContactDeleteView.as_view(), name='contact-delete'),
	path('api/', include(router.urls)),
]