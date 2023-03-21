from django.conf import settings
from django.db import models

import uuid


class Article(models.Model):
    """Text: Anything that can be read by a user."""

    uuid = models.UUIDField(
        db_index=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    article_html = models.TextField(help_text="HTML / rich-text from rich-text editor.")
    article_json = models.JSONField(help_text="JSON output from tiptap / ProseMirror.")
    is_published = models.BooleanField(help_text="If true, others can read it.")


class Annotation(models.Model):
    """Annotation: Contains highlight and optional comment."""

    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    highlight_start = models.PositiveIntegerField()
    highlight_end = models.PositiveIntegerField()
    highlight_backward = models.BooleanField(default=False)
    comment_html = models.TextField(
        blank=True, help_text="HTML / rich-text from rich-text editor."
    )
    comment_json = models.JSONField(
        blank=True, help_text="JSON output from tiptap / ProseMirror.", null=True
    )
    is_public = models.BooleanField(help_text="If true, others can read it.")
