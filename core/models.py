from ctypes import create_string_buffer
import datetime
import uuid

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.timezone import make_aware

from treebeard.mp_tree import MP_Node


class Article(MP_Node):
    """Text: Anything that can be read by a user."""

    uuid = models.UUIDField(
        db_index=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    author = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    article_html = models.TextField(
        blank=True, help_text="HTML output from WYSIWYG editor."
    )
    article_json = models.JSONField(
        blank=True, null=True, help_text="JSON output specific to ProseMirror."
    )
    article_text = models.TextField(
        blank=True, help_text="Text output from WYSIWYG editor."
    )

    @property
    def children(self):
        return self.get_children()

    @property
    def level(self):
        """Get depth of node. The field name 'depth' doesn't work."""
        return self.get_depth()

    @property
    def next(self):
        """Get next node."""
        try:
            if self.get_first_child():
                return self.get_first_child()
            if self.get_next_sibling():
                return self.get_next_sibling()
            current_node = self
            while current_node:
                parent = current_node.get_parent()
                if parent and parent.get_next_sibling():
                    return parent.get_next_sibling()
                current_node = parent
            return None
        except ObjectDoesNotExist:
            return None

    @property
    def prev(self):
        """Get previous node."""
        try:
            if self.get_prev_sibling():
                current_node = self.get_prev_sibling()
                while current_node:
                    child = current_node.get_last_child()
                    if child and child.get_children().count() == 0:
                        return child
                    if child is None:
                        return current_node
                    current_node = child.get_last_child()
            if self.get_parent():
                return self.get_parent()
            return None
        except ObjectDoesNotExist:
            return None

    @property
    def slugs(self):
        """Get list of slugs of ancestor node."""
        parent = self.get_parent()
        if parent:
            # .append() returns None since it modifies in place
            # so cannot `return list.append(...)` directly
            parent_slugs = list(parent.slugs)
            parent_slugs.append(str(self.uuid))
            return parent_slugs
        return [str(self.uuid)]

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
    is_public = models.BooleanField(default=False)


class Comment(MP_Node):
    """Comments: Can be either main post or replies."""

    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    annotation = models.ForeignKey(
        Annotation, on_delete=models.CASCADE, related_name="comments"
    )
    created_on = models.DateTimeField(auto_now=True)
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
        return self.get_parent()

    @property
    def children(self):
        return self.get_children()

    def __str__(self):
        return self.comment_html
