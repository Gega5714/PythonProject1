from django.urls import path, include

urlpatterns = [
    path('contacts/', include('contacts.urls')),
    path('users/', include('users.urls')),
]