from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Article, Annotation
from .validators import JSONSchemaValidator


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


HIGHLIGHT_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "backward": {"type": "boolean"},
            "characterRange": {
                "type": "object",
                "properties": {
                    "start": {"type": "integer"},
                    "end": {"type": "integer"},
                },
            },
        },
    },
}


class AnnotationSerializer(serializers.ModelSerializer):
    """Serializer for Annotation model."""

    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), read_only=False, slug_field="uuid"
    )

    def validate_highlight(self, highlight):
        """Validate highlight"""
        JSONSchemaValidator(HIGHLIGHT_SCHEMA)(highlight)
        return highlight

    class Meta:
        model = Annotation
        fields = [
            "id",
            "uuid",
            "user",
            "article",
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
