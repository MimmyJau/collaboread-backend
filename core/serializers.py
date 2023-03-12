from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Document, Annotation


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model."""

    class Meta:
        model = Document
        fields = [
            "id",
            "uuid",
            "user",
            "title",
            "created_on",
            "updated_on",
            "document_html",
            "document_json",
            "is_published",
        ]
        read_only = ["uuid", "created_on", "updated_on"]


class AnnotationSerializer(serializers.ModelSerializer):
    """Serializer for Annotation model."""

    class Meta:
        model = Annotation
        fields = [
            "id",
            "uuid",
            "user",
            "document",
            "created_on",
            "updated_on",
            "highlight",
            "comment_html",
            "comment_json",
            "is_public",
        ]
        read_only = ["uuid", "created_on", "updated_on"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User Model."""

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "uuid",
            "username",
            "date_joined",
            "first_name",
            "last_name",
            "email",
            "is_superuser",
            "is_staff",
            "is_active",
        ]
