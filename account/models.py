import base64
import binascii
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(db_index=True)

    def get_url_safe_uuid(self):
        return base64.urlsafe_b64encode(self._id.bytes).rstrip(b'=').decode('utf-8')

    def set_url_safe_uuid(self, url_safe_uuid):
        try:
            uuid_bytes = base64.urlsafe_b64decode(url_safe_uuid + '==')
            self._id = uuid.UUID(bytes=uuid_bytes)
        except (ValueError, TypeError, binascii.Error):
            raise ValueError("Invalid URL-safe UUID format")

    user_id = property(get_url_safe_uuid, set_url_safe_uuid)
