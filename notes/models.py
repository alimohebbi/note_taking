import base64
import binascii

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractUser

User = get_user_model()


class Note(models.Model):
    NOTE_TYPE = [('I', 'Idea'),
                 ('T', 'Thought'),
                 ('R', 'Reminder')]

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    note_type = models.CharField(max_length=1, choices=NOTE_TYPE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField("create date", default=timezone.now, db_index=True)
    updated_at = models.DateTimeField("update date", null=True)
    remind_at = models.DateTimeField("reminder date", null=True)

    def __str__(self):
        return self.title

    def get_url_safe_uuid(self):
        return base64.urlsafe_b64encode(self._id.bytes).rstrip(b'=').decode('utf-8')

    def set_url_safe_uuid(self, url_safe_uuid):
        try:
            uuid_bytes = base64.urlsafe_b64decode(url_safe_uuid + '==')
            self._id = uuid.UUID(bytes=uuid_bytes)
        except (ValueError, TypeError, binascii.Error):
            raise ValueError("Invalid URL-safe UUID format")

    note_id = property(get_url_safe_uuid, set_url_safe_uuid)


class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, db_index=True)
    recipient_user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField("create date", default=timezone.now, db_index=True)

    def __str__(self):
        return f'Note "{self.note.title}" shared with user "{self.recipient_user.username}"'
