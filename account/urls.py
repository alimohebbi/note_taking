from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name='api-logout'),
    path('login/', obtain_auth_token, name='api_login'),

]
