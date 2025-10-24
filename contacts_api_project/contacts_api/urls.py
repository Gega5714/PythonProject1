from django.contrib.auth import views as auth_views
from django.urls import path, include

from .views import HomeView
from users.views import CustomLoginView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('contacts/', include('contacts.urls')),
    path('users/', include('users.urls')),
]