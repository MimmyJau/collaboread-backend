import datetime
import uuid

from django.conf import settings
from django.db import models

from treebeard.mp_tree import MP_Node


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

    def __str__(self):
        return self.title + " by " + self.user.username


class Annotation(models.Model):
    """Annotation: Contains highlight and optional comment."""

    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    highlight_start = models.PositiveIntegerField()
    highlight_end = models.PositiveIntegerField()
    highlight_backward = models.BooleanField(default=False)


class Comment(MP_Node):
    """Comments: Can be either main post or replies."""

    node_order_by = ["created_on"]

    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    annotation = models.ForeignKey(
        Annotation, on_delete=models.CASCADE, related_name="comments"
    )
    created_on = models.DateTimeField(default=datetime.datetime.now)
    updated_on = models.DateTimeField(auto_now=True)
    comment_html = models.TextField(
        blank=True, help_text="HTML output from rich-text editor."
    )
    comment_json = models.JSONField(
        blank=True, help_text="JSON output from rich-text editor.", null=True
    )
    comment_text = models.TextField(
        blank=True, help_text="Plain-text output from rich-text editor.", default=""
    )

    @property
    def parent(self):
        print("Parent:", self.get_parent())
        return self.get_parent()

    @property
    def children(self):
        print("Children:", self.get_children())
        return self.get_children()

    def __str__(self):
        return self.comment_html
