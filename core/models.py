from slugify import slugify
import uuid

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.timezone import make_aware

from treebeard.mp_tree import MP_Node


"""
Decision to use MP_Node is as follows:
1) We want the entire path of a section in a book to be unique,
2) Uniqueness only requires comparing against siblings,
3) It better matches how we imagine sections and articles to be structured.
4) We want a path field to uniquely identify the resource.
"""


class Article(MP_Node):
    """Text: Anything that can be read by a user."""

    uuid = models.UUIDField(
        db_index=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    slug_section = models.TextField(max_length=50)
    slug_full = models.TextField(max_length=1000, unique=True, db_index=True)
    author = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    article_html = models.TextField(help_text="HTML output from WYSIWYG editor.")
    article_json = models.JSONField(
        blank=True, null=True, help_text="JSON output specific to ProseMirror."
    )
    article_text = models.TextField(
        blank=True, help_text="Text output from WYSIWYG editor."
    )
    hidden = models.BooleanField(default=False)

    @property
    def children(self):
        """Used by TOC serializer to get all articles"""
        return self.get_children()

    @property
    def level(self):
        """Used by TOC serializer to determine indent level. Note that fidle name 'depth' doesn't work."""
        return self.get_depth()

    @property
    def next(self):
        """Get next node (excluding root nodes)."""
        try:
            if self.get_first_child():
                return self.get_first_child()
            if self.get_next_sibling():
                return self.get_next_sibling()
            current_node = self
            while current_node:
                parent = current_node.get_parent()
                if not parent or parent.is_root():
                    # Don't want to jump to another book.
                    return None
                if parent and parent.get_next_sibling():
                    return parent.get_next_sibling()
                current_node = parent
            return None
        except ObjectDoesNotExist:
            return None

    @property
    def prev(self):
        """Get previous node (excluding root nodes)."""
        try:
            if self.is_root():
                # Don't want it linking to a previous book
                return None
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

    # Don't think this is used anywhere
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

    def update_slug(self):
        slug = slugify(self.title, max_length=50)
        siblings = self.get_siblings().exclude(uuid=self.uuid)
        count = 2
        while True:
            # Don't use `if results is not None:` because that will check
            # for None explicitly, which an empty queryset is not.
            # on the other hand, an empty queryset is falsey.
            filtered_siblings = siblings.filter(slug_section=slug)
            if not filtered_siblings:
                break
            slug = f"{slug}-{count}"
            count += 1
        self.slug_section = slug

    def update_path(self):
        if self.is_root():
            self.slug_full = self.slug_section
            return
        parent = self.get_parent()
        self.slug_full = parent.slug_full + "/" + self.slug_section

    @classmethod
    def create_root(cls, **data):
        return cls.add_root(**data)

    @classmethod
    def create_child(cls, parent_path, **data):
        # TODO throw error if parent does not exist
        parent = Article.objects.get(slug_full=parent_path)
        return parent.add_child(**data)

    def save(self, *args, **kwargs):
        """
        This method is called by .add_root(), .add_child(), and .update().
        """
        self.update_slug()
        self.update_path()
        super().save(*args, **kwargs)
        children = self.get_children()
        if not children:
            return
        for child in children:
            # if child's path != parent's path + child's slug
            # then update child's path
            if child.slug_full != self.slug_full + "/" + child.slug_section:
                child.save()

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


class Bookmark(models.Model):
    """Bookmark: Keeps track of user's location in book usng range"""

    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="bookmarks"
    )
    # Use "+" for related_name to avoid reverse accessor for this field
    # Source: https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.ForeignKey.related_name
    book = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="+")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    highlight_start = models.PositiveIntegerField()
    highlight_end = models.PositiveIntegerField()
