from django.shortcuts import render

from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete() # If you are using token-based authentication, you can clear the token.
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
