import uuid

from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from notes.factories import NoteFactory, note_data_generator, SharedNoteFactory
from notes.models import Note, User


class NoteModelTest(TestCase):
    def test_note_str(self):
        note = NoteFactory.create()
        self.assertEqual(note.title, str(note))

    def test_share_note_str(self):
        shared_note = SharedNoteFactory.create()
        self.assertEqual(str(shared_note),
                         f'Note "{shared_note.note.title}" shared with user "{shared_note.recipient_user.username}"')
