from notes.factories import UserFactory, NoteFactory

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Custom management command description'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Specify users numbers')
        parser.add_argument('--notes', type=int, default=10, help='Specify notes per user numbers')


    def handle(self, *args, **options):
        user_num = options['users']
        note_num = options['notes']

        populate_database(user_num, note_num)
        self.stdout.write(self.style.SUCCESS(f'{user_num} user(s) created with {note_num} note(s) each.'))


def populate_database(users_num, note_num_per_user):
    for i in range(users_num):
        user = UserFactory.create()
        NoteFactory.create_batch(size=note_num_per_user, user=user)



