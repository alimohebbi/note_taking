import factory
from django.forms import model_to_dict

from account.serializers import UserSerializer
from notes.factories import UserFactory, NoteFactory, SharedNoteFactory

from django.core.management.base import BaseCommand
from faker import Faker

from notes.serializers import NoteSerializer


class Command(BaseCommand):
    help = 'Custom management command description'

    def add_arguments(self, parser):
        parser.add_argument('--size', type=int, default=10, help='Specify batche size')

    def get_user_dict(self, user):
        password = Faker().password()
        user.set_password(password)
        user.save()
        return {'email': user.email, 'user_name': user.username, 'password': password}

    def get_note_dict(self, note):
        return {'note_id': note.note_id, 'user': self.get_user_dict(note.user)}

    def handle(self, *args, **options):
        batch_size = options['size']

        writer = UserFactory.create()
        NoteFactory.create_batch(size=batch_size, user=writer)

        highly_shared = NoteFactory.create(user=writer)
        SharedNoteFactory.create_batch(size=batch_size, note=highly_shared)

        highly_received = UserFactory.create()
        SharedNoteFactory.create_batch(size=batch_size, recipient_user=highly_received)

        message = f'\nPro writer User is:\n {self.get_user_dict(highly_shared.user)} \n\n'
        message += f'Pro shared Note is:\n { {"note_id": highly_shared.note_id}}\n\n'
        message += f'Pro recipient User is:\n {self.get_user_dict(highly_received)}\n\n'
        self.stdout.write(self.style.SUCCESS(message))

