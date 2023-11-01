from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from notes.factories import user_data_generator, UserFactory
from note_taking.config_vars import OBJECTS_BATCH_SIZE


class AccountAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory.create()
        UserFactory.create_batch(OBJECTS_BATCH_SIZE)

    def authenticate(self, user):
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def test_post_register_user_successful(self):
        user_data = user_data_generator()
        url = reverse('api_register')
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_data = user_data_generator()
        user_data.pop('email')
        url = reverse('api_register')
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_register_user_error_validation(self):
        user_data = user_data_generator()
        user_data.pop('username')
        url = reverse('api_register')
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_data = user_data_generator()
        user_data.pop('password')
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_logout_user_successful(self):
        self.authenticate(self.user)
        url = reverse('api_logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_logout_user_unauthorized(self):
        url = reverse('api_logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
