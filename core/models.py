from django.conf import settings
from django.db import models

import uuid


class Document(models.Model):
    """Text: Anything that can be read by a user."""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    document_html = models.TextField(
        help_text="HTML / rich-text from rich-text editor."
    )
    document_json = models.JSONField(help_text="JSON output from tiptap / ProseMirror.")
    is_published = models.BooleanField(help_text="If true, others can read it.")


class Annotation(models.Model):
    """Annotation: Contains highlight and optional comment."""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    highlight = models.CharField(
        max_length=200, help_text="Serialized range by Rangy library"
    )
    comment_html = models.TextField(help_text="HTML / rich-text from rich-text editor.")
    comment_json = models.JSONField(help_text="JSON output from tiptap / ProseMirror.")
    is_public = models.BooleanField(help_text="If true, others can read it.")
