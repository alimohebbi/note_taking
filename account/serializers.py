from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.util import UrlSafeUUIDField

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # user_id = UrlSafeUUIDField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_id']
        extra_kwargs = {'user_id': {'required': False}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.email = validated_data['email']
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
