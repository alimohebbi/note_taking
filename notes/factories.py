import factory
from django.contrib.auth.models import User
from django.forms import model_to_dict

from notes.models import Note


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    email = factory.Faker('email')


class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text', max_nb_chars=200)
    user = factory.SubFactory(UserFactory)


def note_data_generator():
    note_stub = NoteFactory.build()
    new_note_data = model_to_dict(note_stub)
    new_note_data.pop('id')
    new_note_data.pop('user')
    return new_note_data
