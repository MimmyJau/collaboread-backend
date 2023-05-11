from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest_framework_recursive.fields import RecursiveField

from .models import ArticleMP, Article, Annotation, Comment
from accounts.serializers import PublicUserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for Article model."""

    user = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), read_only=False, slug_field="username"
    )

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


class ArticleListSerializer(serializers.ModelSerializer):
    """Serializer for Article Model."""

    user = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), read_only=False, slug_field="username"
    )

    class Meta:
        model = ArticleMP
        fields = [
            "uuid",
            "user",
            "title",
            "created_on",
            "updated_on",
        ]
        read_only = ["id", "uuid", "created_on", "updated_on"]


class ArticleMPSerializer(serializers.ModelSerializer):
    """Serializer for Article Model."""

    user = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), read_only=False, slug_field="username"
    )
    prev = serializers.SerializerMethodField(method_name="get_prev")
    next = serializers.SerializerMethodField(method_name="get_next")

    class Meta:
        model = ArticleMP
        fields = [
            "uuid",
            "user",
            "title",
            "created_on",
            "updated_on",
            "article_html",
            "article_json",
            "article_text",
            "level",
            "prev",
            "next",
        ]
        read_only = ["id", "uuid", "created_on", "updated_on", "prev", "next"]
        extra_kwargs = {
            "article_json": {"write_only": True},
            "article_text": {"write_only": True},
        }

    def get_next(self, obj):
        next_node = obj.next
        if next_node:
            return next_node.slugs
        return None

    def get_prev(self, obj):
        prev_node = obj.prev
        if prev_node:
            return prev_node.slugs
        return None


class TableOfContentsSerializer(serializers.ModelSerializer):
    """Serializer for Table of Contents."""

    children = RecursiveField(many=True, read_only=True)

    class Meta:
        model = ArticleMP
        fields = [
            "uuid",
            "title",
            "level",
            "children",
        ]
        read_only = ["uuid", "title", "level", "children"]


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""

    user = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), read_only=False, slug_field="username"
    )
    article = serializers.SlugRelatedField(
        queryset=ArticleMP.objects.all(), read_only=False, slug_field="uuid"
    )
    annotation = serializers.SlugRelatedField(
        queryset=Annotation.objects.all(), read_only=False, slug_field="uuid"
    )

    """
    Since parent field is read-only in MP_Tree, we have to use a
    custom field parent_uuid that can do both read and write.

    If we didn't use custom field and tried to use built-in parent field,
    we would have access to the parent field when deciding whether to
    use add_root or add-child in custom `.create()` method (since parent
    field is read-only).

    Notes:
    - In custom `.create()` method, we only use parent_uuid for deciding
      which django-treebeard method to call,
    - In custom `.to_representation()` method, we fetch uuid to include
      in json response.
    """
    parent_uuid = serializers.UUIDField(required=True, allow_null=True)
    children = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "uuid",
            "user",
            "article",
            "annotation",
            "parent_uuid",
            "children",
            "created_on",
            "updated_on",
            "comment_html",
            "comment_json",
            "comment_text",
        ]
        read_only = ["uuid", "created_on", "updated_on"]

    def create(self, validated_data):
        parent_uuid = validated_data.pop("parent_uuid", None)
        if parent_uuid is not None:
            parent = Comment.objects.get(uuid=parent_uuid)
            return parent.add_child(**validated_data)
        return Comment.add_root(**validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["parent_uuid"] = instance.parent.uuid if instance.parent else None
        return rep


class AnnotationReadSerializer(serializers.ModelSerializer):
    """Serializer for Reading Annotation model."""

    user = PublicUserSerializer(read_only=True)
    article = serializers.SlugRelatedField(
        queryset=ArticleMP.objects.all(), read_only=False, slug_field="uuid"
    )
    comments = CommentSerializer(read_only=True, many=True)

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
        queryset=ArticleMP.objects.all(), read_only=False, slug_field="uuid"
    )
    comments = CommentSerializer(many=True, read_only=True)

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
