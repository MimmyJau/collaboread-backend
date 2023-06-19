from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers


class UserSerializer(RegisterSerializer):
    """Serializer for User Model."""

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "uuid",
            "username",
            "email",
            "date_joined",
        ]
        read_only = ["id", "uuid", "date_joined", "is_superuser", "is_staff"]


class PublicUserSerializer(serializers.ModelSerializer):
    """Serializer for Public-Facing User Model."""

    class Meta:
        model = get_user_model()
        fields = [
            "uuid",
            "username",
        ]
        read_only = ["uuid", "username"]
