from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from .views import UserRegistrationView

urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name='api_logout'),
    path('login/', obtain_auth_token, name='api_login'),
    path('register/', UserRegistrationView.as_view(), name='api_register')
]
