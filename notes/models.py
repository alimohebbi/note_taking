from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Note(models.Model):
    NOTE_TYPE = [('I', 'Idea'),
                 ('T', 'Thought'),
                 ('R', 'Reminder')]

    note_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    note_type = models.CharField(max_length=1, choices=NOTE_TYPE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField("create date", default=timezone.now, db_index=True)
    updated_at = models.DateTimeField("update date", null=True)
    remind_at = models.DateTimeField("reminder date", null=True)

    def __str__(self):
        return self.title


class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, db_index=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField("create date", default=timezone.now, db_index=True)


    def __str__(self):
        return f'Note "{self.note.title}" shared with user "{self.recipient.username}"'
