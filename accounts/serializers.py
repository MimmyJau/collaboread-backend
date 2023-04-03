from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
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
