from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'content', '_id', 'remind_at', 'note_type', 'created_at']
        extra_kwargs = {'user': {'required': False}}

    def validate_note_type(self, value):
        remind_at = self.initial_data.get('remind_at')
        if value == 'R' and remind_at is None:
            raise serializers.ValidationError("remind_at is required for Reminder.")
        return value


class ListNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', '_id', 'created_at']
