from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import UserRegistrationSerializer
from common.messages import AccountMessages


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # If you are using token-based authentication, you can clear the token.
        return Response(AccountMessages.LOGOUT_SUCCESS, status=status.HTTP_200_OK)


class UserRegistrationView(CreateAPIView):
    permission_classes = []
    serializer_class = UserRegistrationSerializer
