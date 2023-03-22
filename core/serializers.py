from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Article, Annotation


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for Article model."""

    class Meta:
        model = Article
        fields = [
            "id",
            "uuid",
            "user",
            "title",
            "created_on",
            "updated_on",
            "article_html",
            "article_json",
            "is_published",
        ]
        read_only = ["uuid", "created_on", "updated_on"]


class AnnotationSerializer(serializers.ModelSerializer):
    """Serializer for Annotation model."""

    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), read_only=False, slug_field="uuid"
    )

    class Meta:
        model = Annotation
        fields = [
            "id",
            "uuid",
            "user",
            "article",
            "created_on",
            "updated_on",
            "highlight_start",
            "highlight_end",
            "highlight_backward",
            "comment_html",
            "comment_json",
            "is_public",
        ]
        read_only = ["created_on", "updated_on"]


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
