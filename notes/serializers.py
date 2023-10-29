from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'description', 'id']
        extra_kwargs = {'user': {'required': False}}


class ListNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'id']
