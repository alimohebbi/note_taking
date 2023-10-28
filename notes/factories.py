import factory
from django.contrib.auth.models import User
from django.forms import model_to_dict
from factory import fuzzy

from notes.models import Note


class UniqueUsernameProvider(factory.faker.Faker):
    def unique_username(self):
        username = factory.fuzzy.FuzzyText(length=10).fuzz()
        while User.objects.filter(username=username).exists():
            username = factory.fuzzy.FuzzyText(length=10).fuzz()
        return username


factory.Faker.add_provider(UniqueUsernameProvider)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('unique_username')
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


def user_data_generator():
    user_obj = UserFactory.build()
    new_user_data = model_to_dict(user_obj)
    new_user_data.pop('id')
    new_user_data.pop('last_login')
    return new_user_data
