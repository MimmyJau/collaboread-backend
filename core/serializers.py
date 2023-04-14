from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Article, Annotation, Comment
from accounts.serializers import PublicUserSerializer


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


class CommentReadSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""

    user = PublicUserSerializer(read_only=True)
    annotation = serializers.SlugRelatedField(
        queryset=Annotation.objects.all(), read_only=False, slug_field="uuid"
    )
    reply_to = serializers.SlugRelatedField(
        queryset=Comment.objects.all(), read_only=False, slug_field="uuid"
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "uuid",
            "user",
            "annotation",
            "reply_to",
            "created_on",
            "updated_on",
            "comment_html",
            "comment_json",
        ]
        read_only = ["uuid", "created_on", "updated_on"]


class CommentWriteSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""

    user = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), read_only=False, slug_field="username"
    )
    reply_to = serializers.SlugRelatedField(
        queryset=Comment.objects.all(), read_only=False, slug_field="uuid"
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "annotation",
            "reply_to",
            "created_on",
            "updated_on",
            "comment_html",
            "comment_json",
        ]
        read_only = ["uuid", "created_on", "updated_on"]


class AnnotationReadSerializer(serializers.ModelSerializer):
    """Serializer for Reading Annotation model."""

    user = PublicUserSerializer(read_only=True)
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), read_only=False, slug_field="uuid"
    )
    comments = CommentReadSerializer(read_only=True, many=True)

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
            "comments",
        ]
        read_only = ["id", "user", "created_on", "updated_on"]


class AnnotationWriteSerializer(serializers.ModelSerializer):
    """Serializer for Writing Annotation model."""

    user = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), read_only=False, slug_field="username"
    )
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), read_only=False, slug_field="uuid"
    )
    comments = CommentWriteSerializer(many=True, read_only=True)

    def validate(self, attrs):
        """Ensure highlight contains at least one character"""
        if attrs["highlight_start"] >= attrs["highlight_end"]:
            raise serializers.ValidationError("End must be greater than start")
        return attrs

    class Meta:
        model = Annotation
        fields = [
            "uuid",
            "user",
            "article",
            "created_on",
            "updated_on",
            "highlight_start",
            "highlight_end",
            "highlight_backward",
            "comments",
        ]
