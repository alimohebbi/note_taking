import binascii
import uuid


import base64
from rest_framework import serializers

def is_vali_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


class UrlSafeUUIDField(serializers.Field):
    def to_representation(self, obj):
        return base64.urlsafe_b64encode(obj.bytes).rstrip(b'=').decode('utf-8')

    def to_internal_value(self, data):
        try:
            uuid_bytes = base64.urlsafe_b64decode(data + '==')
            return uuid.UUID(bytes=uuid_bytes)
        except (ValueError, TypeError, binascii.Error):
            raise serializers.ValidationError("Invalid URL-safe UUID format")


