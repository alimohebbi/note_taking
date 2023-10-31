import factory
from django.forms import model_to_dict
from django.utils import timezone
from factory import fuzzy, Faker

from notes.models import Note, User


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

    note_type = Faker('random_element', elements=[choice[0] for choice in Note.NOTE_TYPE])

    title = factory.Faker('sentence', nb_words=3)
    content = factory.Faker('text', max_nb_chars=200)
    user = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.Faker('date_time_this_decade', before_now=True, after_now=True, tzinfo=timezone.utc)
    remind_at = factory.Faker('date_time_this_decade', before_now=False, after_now=True, tzinfo=timezone.utc)

    @factory.post_generation
    def set_remind_at(obj, create, extracted, **kwargs):
        if obj.note_type == 'R':
            obj.reminder_at = factory.Faker('date_time_this_decade', before_now=False, after_now=True,
                                            tzinfo=timezone.utc)
        else:
            obj.reminder_at = None


def note_data_generator(note_type=None):
    if note_type:
        note_stub = NoteFactory.build(note_type=note_type)
    else:
        note_stub = NoteFactory.build()
    new_note_data = model_to_dict(note_stub)
    new_note_data.pop('user')
    return new_note_data


def user_data_generator():
    user_obj = UserFactory.build()
    new_user_data = model_to_dict(user_obj)
    new_user_data.pop('id')
    new_user_data.pop('last_login')
    return new_user_data
