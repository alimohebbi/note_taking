import uuid

from django.test import TestCase
from django.urls import reverse
from faker import Faker, factory
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from note_taking.config_vars import OBJECTS_BATCH_SIZE
from notes.factories import NoteFactory, note_data_generator, SharedNoteFactory, UserFactory
from notes.models import Note, User, SharedNote

PAGINATION_PARAM = f'?page=2&page_size=8'


class NoteSharingAPITest(TestCase):
    def authenticate(self, user):
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def setUp(self):
        self.client = APIClient()
        SharedNoteFactory.create_batch(OBJECTS_BATCH_SIZE)
        self.note = NoteFactory.create()
        self.user = self.note.user
        self.shared_note = NoteFactory.create(user=self.user)
        SharedNoteFactory.create_batch(size=OBJECTS_BATCH_SIZE, note=self.shared_note)

    def test_get_share_with_user_list_successful(self):
        self.authenticate(self.user)
        url = reverse('share_with', args=[self.shared_note.note_id]) + PAGINATION_PARAM
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 8)

    def test_get_share_with_user_list_unauthorized_error(self):
        url = reverse('share_with', args=[self.shared_note.note_id]) + PAGINATION_PARAM
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_share_with_user_list_forbidden_error(self):
        forbidden_user = UserFactory.create()
        self.authenticate(forbidden_user)
        url = reverse('share_with', args=[self.shared_note.note_id]) + PAGINATION_PARAM
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_share_with_user_successful(self):
        self.authenticate(self.user)
        recipient_user = UserFactory.create()
        url = reverse('share_with', args=[self.note.note_id])
        data = {'email': str(recipient_user.email)}
        response = self.client.post(url, data=data)
        is_shared = SharedNote.objects.filter(note=self.note, recipient_user=recipient_user).exists()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(is_shared)

    def test_post_share_with_user_unauthorized_error(self):
        recipient_user = UserFactory.create()
        url = reverse('share_with', args=[self.note.note_id])
        data = {'email': str(recipient_user.email)}
        response = self.client.post(url, data=data)
        is_shared = SharedNote.objects.filter(note=self.note, recipient_user=recipient_user).exists()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(not is_shared)

    def test_post_share_with_user_forbidden_error(self):
        forbidden_user = UserFactory.create()
        self.authenticate(forbidden_user)
        recipient_user = UserFactory.create()
        url = reverse('share_with', args=[self.note.note_id])
        data = {'email': str(recipient_user.email)}
        response = self.client.post(url, data=data)
        is_shared = SharedNote.objects.filter(note=self.note, recipient_user=recipient_user).exists()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(not is_shared)

    def test_post_share_with_user_not_found_error(self):
        # @todo user not found
        self.authenticate(self.user)
        url = reverse('share_with', args=[self.note.note_id])
        data = {'email': str(Faker().email())}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        fake_id = uuid.uuid4()
        url = reverse('share_with', args=[fake_id])
        data = {'email': self.user.email}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        fake_invalid_id = Faker().word()
        url = reverse('share_with', args=[fake_invalid_id])
        data = {'email': self.user.user_id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_share_with_user_validation_error(self):
        self.authenticate(self.user)
        url = reverse('share_with', args=[self.note.note_id])
        data = {'email': Faker().word()}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_share_with_user_successful(self):
        self.authenticate(self.user)
        shared_note_record = SharedNoteFactory.create(note=self.shared_note)
        url = reverse('share_with', args=[self.shared_note.note_id])
        response = self.client.delete(url, data={'email': shared_note_record.recipient_user.email})
        is_shared = SharedNote.objects.filter(id=shared_note_record.id).exists()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not is_shared)

    def test_delete_share_with_user_unauthorized_error(self):
        shared_note_record = SharedNoteFactory.create(note=self.shared_note)
        url = reverse('share_with', args=[self.shared_note.note_id])
        response = self.client.delete(url, data={'email': shared_note_record.recipient_user.email})
        is_shared = SharedNote.objects.filter(id=shared_note_record.id).exists()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(is_shared)

    def test_delete_share_with_user_forbidden_error(self):
        forbidden_user = UserFactory.create()
        self.authenticate(forbidden_user)
        shared_note_record = SharedNoteFactory.create(note=self.shared_note)
        url = reverse('share_with', args=[self.shared_note.note_id])
        response = self.client.delete(url, data={'email': shared_note_record.recipient_user.email})
        is_shared = SharedNote.objects.filter(id=shared_note_record.id).exists()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(is_shared)

    def test_delete_share_with_user_validation_error(self):
        self.authenticate(self.user)
        shared_note_record = SharedNoteFactory.create(note=self.shared_note)
        url = reverse('share_with', args=[self.shared_note.note_id])
        response = self.client.delete(url, data={'email': Faker().word()})
        is_shared = SharedNote.objects.filter(id=shared_note_record.id).exists()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(is_shared)

    def test_delete_share_with_user_not_found_error(self):
        self.authenticate(self.user)
        shared_note_record = SharedNoteFactory.create(note=self.shared_note)
        url = reverse('share_with', args=[self.shared_note.note_id])
        response = self.client.delete(url, data={'email': Faker().email()})
        is_shared = SharedNote.objects.filter(id=shared_note_record.id).exists()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(is_shared)

        fake_id = uuid.uuid4()
        url = reverse('share_with', args=[fake_id])
        response = self.client.delete(url, data={'email': shared_note_record.recipient_user.email})
        is_shared = SharedNote.objects.filter(id=shared_note_record.id).exists()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(is_shared)

        fake_id = Faker().word()
        url = reverse('share_with', args=[fake_id])
        response = self.client.delete(url, data={'email': shared_note_record.recipient_user.email})
        is_shared = SharedNote.objects.filter(id=shared_note_record.id).exists()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(is_shared)

    def test_get_shared_with_curren_user_note_list_successful(self):
        self.authenticate(self.user)
        SharedNoteFactory.create_batch(size=OBJECTS_BATCH_SIZE, recipient_user=self.user)
        url = reverse('shared_with_me') + PAGINATION_PARAM
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 8)

    def test_get_shared_with_current_user_note_list_unauthorized_error(self):
        SharedNoteFactory.create_batch(size=OBJECTS_BATCH_SIZE, recipient_user=self.user)
        url = reverse('shared_with_me') + PAGINATION_PARAM
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_shared_with_user_note_successful(self):
        self.authenticate(self.user)
        shared_note_record = SharedNoteFactory.create(recipient_user=self.user)
        url = reverse('shared_with_me')
        response = self.client.delete(url, data={'note_id': shared_note_record.note.note_id})
        is_shared = SharedNote.objects.filter(id=shared_note_record.id).exists()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not is_shared)

    def test_delete_shared_with_user_error_unautorizerd(self):
        shared_note_record = SharedNoteFactory.create(recipient_user=self.user)
        url = reverse('shared_with_me')
        response = self.client.delete(url, data={'note_id': shared_note_record.note.note_id})
        is_shared = SharedNote.objects.filter(id=shared_note_record.id).exists()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(is_shared)

    def test_delete_shared_with_user_error_validation(self):
        self.authenticate(self.user)
        shared_note_record = SharedNoteFactory.create(recipient_user=self.user)
        url = reverse('shared_with_me')
        response = self.client.delete(url, data={'note_id': Faker().word()})
        is_shared = SharedNote.objects.filter(id=shared_note_record.id).exists()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(is_shared)
