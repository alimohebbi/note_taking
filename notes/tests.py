from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from notes.factories import NoteFactory, note_data_generator
from notes.models import Note


class NoteAPITest(TestCase):
    def authenticate(self, user):
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def setUp(self):
        self.client = APIClient()
        NoteFactory.create_batch(50)
        self.note = NoteFactory.create()
        self.user = self.note.user

    def test_get_list_successful(self):
        NoteFactory.create_batch(size=50, user=self.user)
        self.authenticate(self.user)
        url = reverse('note_list') + f'?page=2&page_size=8'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 8)

    def test_get_list_successful_unauthorized_error(self):
        url = reverse('note_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_idea_successful(self):
        self.post_note_successful('I')

    def test_post_reminder_successful(self):
        self.post_note_successful('R')

    def test_post_thought_successful(self):
        self.post_note_successful('T')

    def post_note_successful(self, note_type):
        self.authenticate(self.user)
        new_note_data = note_data_generator(note_type)
        url = reverse('note_list')
        user_notes_number_before = Note.objects.filter(user=self.user).count()
        response = self.client.post(url, new_note_data)
        user_notes_number_after = Note.objects.filter(user=self.user).count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_notes_number_after, user_notes_number_before + 1)

    def test_post_note_validation_error(self):
        self.authenticate(self.user)
        faker = Faker()
        url = reverse('note_list')
        new_note = {'content': faker.sentence(nb_words=3), 'note_type': 'I'}
        response = self.client.post(url, new_note)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        new_note = {'title': faker.sentence(nb_words=3), 'note_type': 'I'}
        response = self.client.post(url, new_note)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        new_note = {'title': faker.sentence(nb_words=3), 'note_type': 'R', 'content': faker.sentence(nb_words=3)}
        response = self.client.post(url, new_note)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_note_unauthorized_error(self):
        new_note = note_data_generator()
        url = reverse('note_list')
        response = self.client.post(url, new_note)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detail_successful(self):
        self.authenticate(self.user)
        url = reverse('note_detail', args=[self.note.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.note.id)
        self.assertEqual(response.data['title'], self.note.title)
        self.assertEqual(response.data['content'], self.note.content)

    def test_get_detail_unauthorized_error(self):
        url = reverse('note_detail', args=[self.note.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detail_forbidden_error(self):
        forbidden_user = User.objects.create(username='joe', password='1234', email='joe@gmail.com')
        self.authenticate(forbidden_user)
        url = reverse('note_detail', args=[self.note.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_detail_not_found_error(self):
        self.authenticate(self.user)
        url = reverse('note_detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_detail_successful(self):
        self.authenticate(self.user)
        url = reverse('note_detail', args=[self.note.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_detail_unauthorized_error(self):
        url = reverse('note_detail', args=[self.note.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_detail_forbidden_error(self):
        forbidden_user = User.objects.create(username='joe', password='1234', email='joe@gmail.com')
        self.authenticate(forbidden_user)
        url = reverse('note_detail', args=[self.note.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_delete_not_found_error(self):
        self.authenticate(self.user)
        url = reverse('note_detail', args=[9999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_detail_successful(self):
        self.authenticate(self.user)
        new_data = note_data_generator()
        url = reverse('note_detail', args=[self.note.id])
        response = self.client.put(url, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_detail_validation_error(self):
        self.authenticate(self.user)
        faker = Faker()
        url = reverse('note_detail', args=[self.note.id])
        new_note_data = {'description': faker.sentence(nb_words=3)}
        response = self.client.put(url, new_note_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        new_note_data = {'title': faker.sentence(nb_words=3)}
        response = self.client.put(url, new_note_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_detail_unauthorized_error(self):
        url = reverse('note_detail', args=[self.note.id])
        new_data = note_data_generator()
        response = self.client.put(url, new_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_detail_forbidden_error(self):
        forbidden_user = User.objects.create(username='joe', password='1234', email='joe@gmail.com')
        self.authenticate(forbidden_user)
        new_data = note_data_generator()
        url = reverse('note_detail', args=[self.note.id])
        response = self.client.put(url, new_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_detail_not_found_error(self):
        self.authenticate(self.user)
        url = reverse('note_detail', args=[9999])
        new_data = note_data_generator()
        response = self.client.put(url, new_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NoteModelTest(TestCase):
    def test_str(self):
        note = NoteFactory.create()
        self.assertEqual(note.title, str(note))
