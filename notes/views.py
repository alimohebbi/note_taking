from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import UserSerializer
from common.messages import NoteMessages
from common.pagination import CustomPagination
from notes.models import Note, SharedNote, User
from notes.serializers import NoteSerializer, ListNoteSerializer, EmailSerializer, SharedNoteSerializer, NoteIdSerializer


class NoteList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_set = Note.objects.filter(user=request.user).order_by('-created_at')
        paginator = CustomPagination()
        paginated_query = paginator.paginate_queryset(query_set, request)
        serializer = ListNoteSerializer(paginated_query, many=True)
        return Response(paginator.get_paginated_response(serializer.data))

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, note_id):
        note = get_object_or_404(Note, pk=note_id)
        if note.user != request.user:
            return Response(NoteMessages.FORBIDDEN_ACCESS, status=status.HTTP_403_FORBIDDEN)

        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, note_id):
        note = get_object_or_404(Note, pk=note_id)
        if note.user != request.user:
            return Response(NoteMessages.FORBIDDEN_MODIFY, status=status.HTTP_403_FORBIDDEN)

        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            note.updated_at = str(timezone.now)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        note = get_object_or_404(Note, pk=note_id)
        if note.user != request.user:
            return Response(NoteMessages.FORBIDDEN_DELETE, status=status.HTTP_403_FORBIDDEN)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShareNoteWithDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, note_id):
        note = get_object_or_404(Note, pk=note_id)
        if note.user != request.user:
            return Response(NoteMessages.FORBIDDEN_MODIFY, status=status.HTTP_403_FORBIDDEN)

        query_set = User.objects.filter(sharednote__note=note).order_by('-sharednote__created_at')
        paginator = CustomPagination()
        paginated_query = paginator.paginate_queryset(query_set, request)
        serializer = UserSerializer(paginated_query, many=True)
        return Response(paginator.get_paginated_response(serializer.data))

    def post(self, request, note_id):
        email_serializer = EmailSerializer(data=request.data)

        note = get_object_or_404(Note, pk=note_id)
        if note.user != request.user:
            return Response(NoteMessages.FORBIDDEN_MODIFY, status=status.HTTP_403_FORBIDDEN)

        if email_serializer.is_valid():
            user = get_object_or_404(User, email=email_serializer.validated_data.get('email'))
            shared_note = SharedNote(recipient=user, note=note)
            shared_note.save()
            shared_note_serializer = SharedNoteSerializer(instance=shared_note)
            return Response(shared_note_serializer.data, status=status.HTTP_201_CREATED)
        return Response(email_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        email_serializer = EmailSerializer(data=request.data)

        note = get_object_or_404(Note, pk=note_id)
        if note.user != request.user:
            return Response(NoteMessages.FORBIDDEN_MODIFY, status=status.HTTP_403_FORBIDDEN)

        if email_serializer.is_valid():
            user = get_object_or_404(User, email=email_serializer.validated_data.get('email'))
            SharedNote.objects.filter(recipient=user, note=note).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(email_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SharedNoteWithMeDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_set = Note.objects.filter(sharednote__recipient=request.user).order_by('-sharednote__created_at')
        paginator = CustomPagination()
        paginated_query = paginator.paginate_queryset(query_set, request)
        serializer = ListNoteSerializer(paginated_query, many=True)
        return Response(paginator.get_paginated_response(serializer.data))

    def delete(self, request):
        note_id_serializer = NoteIdSerializer(data=request.data)
        if note_id_serializer.is_valid():
            note = get_object_or_404(Note, pk=note_id_serializer.data['note_id'])
            SharedNote.objects.filter(recipient=request.user, note=note).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(note_id_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
