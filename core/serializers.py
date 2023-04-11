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
        read_only = ["id", "uuid", "created_on", "updated_on"]


class AnnotationSerializer(serializers.ModelSerializer):
    """Serializer for Annotation model."""

    user = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), slug_field="uuid"
    )
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), read_only=False, slug_field="uuid"
    )

    def validate(self, data):
        """Ensure highlight contains at least one character"""
        if data["highlight_start"] >= data["highlight_end"]:
            raise serializers.ValidationError("End must be greater than start")
        return data

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
        read_only = ["id", "created_on", "updated_on"]
