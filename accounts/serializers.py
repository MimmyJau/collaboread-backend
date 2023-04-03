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
            "date_joined",
            "name",
            "first_name",
            "last_name",
            "email",
        ]
        read_only = ["id", "uuid", "date_joined", "is_superuser", "is_staff"]
