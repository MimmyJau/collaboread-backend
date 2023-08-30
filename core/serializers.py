from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest_framework_recursive.fields import RecursiveField

from bleach import clean

from .models import Article, Annotation, Bookmark, Comment

allowed_tags = [
    "a",
    "b",
    "blockquote",
    "br",
    "code",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "img",
    "li",
    "mark",
    "ol",
    "p",
    "pre",
    "strong",
    "sup",
    "table",
    "tbody",
    "td",
    "th",
    "tr",
    "ul",
]

allowed_attributes = [
    "class",
    "href",
    "src",
    "target",
]


class ArticleListSerializer(serializers.ModelSerializer):
    """Serializer for List of Articles. Don't want to send entire book."""

    user = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), read_only=False, slug_field="username"
    )

    class Meta:
        model = Article
        fields = [
            "uuid",
            "slug_full",
            "user",
            "title",
            "author",
            "created_on",
            "updated_on",
        ]
        read_only = ["uuid", "slug_full", "created_on", "updated_on"]


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for individual Article objects."""

    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    prev = serializers.SerializerMethodField(method_name="get_prev")
    next = serializers.SerializerMethodField(method_name="get_next")

    class Meta:
        model = Article
        fields = [
            "uuid",
            "slug_full",
            "user",
            "title",
            "created_on",
            "updated_on",
            "article_html",
            "article_json",
            "article_text",
            "hidden",
            "level",
            "prev",
            "next",
        ]
        read_only_fields = [
            "uuid",
            "slug_full",
            "created_on",
            "updated_on",
            "prev",
            "next",
        ]
        extra_kwargs = {
            "article_json": {"write_only": True},
            "article_text": {"write_only": True},
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep["article_html"] = clean(
            instance.article_html,
            attributes=allowed_attributes,
            tags=allowed_tags,
            strip=True,
        )
        return rep

    def get_next(self, obj):
        next_node = obj.next
        if next_node:
            return next_node.slug_full
        return None

    def get_prev(self, obj):
        prev_node = obj.prev
        if prev_node:
            return prev_node.slug_full
        return None


class TableOfContentsSerializer(serializers.ModelSerializer):
    """Serializer for Table of Contents. Includes children but the bare-minimum data."""

    children = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            "uuid",
            "slug_full",
            "title",
            "level",
            "children",
        ]
        read_only = ["uuid", "slug_full", "title", "level", "children"]


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""

    user = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), read_only=False, slug_field="username"
    )
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), read_only=False, slug_field="slug_full"
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
        rep["comment_html"] = clean(
            instance.comment_html,
            attributes=allowed_attributes,
            tags=allowed_tags,
            strip=True,
        )
        return rep


class AnnotationSerializer(serializers.ModelSerializer):
    """Serializer for Annotation model."""

    user = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), read_only=False, slug_field="username"
    )
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), read_only=False, slug_field="slug_full"
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
            "is_public",
        ]
        read_only = ["uuid", "created_on", "updated_on"]


class BookmarkSerializer(serializers.ModelSerializer):
    """Serializer for Bookmark model."""

    class Meta:
        model = Bookmark
        fields = [
            "uuid",
            "user",
            "article",
            "book",
            "created_on",
            "updated_on",
            "highlight_start",
            "highlight_end",
        ]
        read_only_fields = ["uuid", "user", "book", "created_on", "updated_on"]

    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), read_only=False, slug_field="slug_full"
    )
    book = serializers.SlugRelatedField(read_only=True, slug_field="slug_full")

    def validate(self, attrs):
        """Ensure highlight contains at least one character"""
        if attrs["highlight_start"] != attrs["highlight_end"]:
            raise serializers.ValidationError(
                {"end": "Range for bookmark must be 0"}, code=400
            )
        return attrs

    def to_internal_value(self, data):
        """Convert structured data to flat data."""
        flat_data = data.copy()
        if "highlight" not in flat_data:
            raise serializers.ValidationError(
                {"highlight": "This field is required."}, code=400
            )
        bookmark_range = flat_data.pop("highlight")
        flat_data["highlight_start"] = bookmark_range[0]["character_range"]["start"]
        flat_data["highlight_end"] = bookmark_range[0]["character_range"]["end"]
        return super().to_internal_value(flat_data)

    def to_representation(self, instance):
        return {
            "uuid": instance.uuid,
            "user": instance.user.username,
            "article": instance.article.slug_full,
            "book": instance.book.slug_full,
            "created_on": instance.created_on,
            "updated_on": instance.updated_on,
            "highlight": [
                {
                    "characterRange": {
                        "start": instance.highlight_start,
                        "end": instance.highlight_end,
                    }
                }
            ],
        }
