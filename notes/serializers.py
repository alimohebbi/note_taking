import base64
import uuid

from django.http import Http404
from rest_framework import serializers

from common.messages import NoteMessages
from common.util import UrlSafeUUIDField
from .models import Note, SharedNote


class NoteSerializer(serializers.ModelSerializer):
    # note_id = UrlSafeUUIDField()

    class Meta:
        model = Note
        fields = ['title', 'content', 'note_id', 'remind_at', 'note_type', 'created_at']
        extra_kwargs = {'user': {'required': False}}

    def validate_note_type(self, value):
        remind_at = self.initial_data.get('remind_at')
        if value == 'R' and remind_at is None:
            raise serializers.ValidationError("remind_at is required for Reminder.")
        return value


class ListNoteSerializer(serializers.ModelSerializer):
    # note_id = UrlSafeUUIDField()

    class Meta:
        model = Note
        fields = ['title', 'note_id', 'created_at']


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class NoteIdSerializer(serializers.Serializer):
    note_id = serializers.CharField()


def convert_urls_safe_to_uuid(value):
    try:
        uuid_bytes = base64.urlsafe_b64decode(value + '==')
        return uuid.UUID(bytes=uuid_bytes)
    except:
        Http404(NoteMessages.NOT_FOUND)


class SharedNoteSerializer(serializers.ModelSerializer):
    note = serializers.SerializerMethodField()
    recipient_user = serializers.SerializerMethodField()

    def get_note(self, obj):
        return obj.note.note_id

    def get_recipient_user(self, obj):
        return obj.recipient_user.user_id

    class Meta:
        model = SharedNote
        fields = ['note', 'recipient_user']
