from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notes.models import Note
from notes.serializers import NoteSerializer


class NoteList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
