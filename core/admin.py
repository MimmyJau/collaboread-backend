from django.contrib import admin
from .models import Article, Annotation, Comment

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


# Register your models here.


class ArticleAdmin(TreeAdmin):
    form = movenodeform_factory(Article)
    list_display = (
        "title",
        "uuid",
    )
    readonly_fields = ["uuid"]
    fieldsets = (
        (
            "Article Info",
            {
                "fields": (
                    "uuid",
                    "slug_section",
                    "slug_full",
                    "user",
                    "title",
                    "author",
                    "article_html",
                    "article_json",
                    "article_text",
                    "hidden",
                )
            },
        ),
        (
            "Move Node",
            {
                "fields": ("_position", "_ref_node_id"),
            },
        ),
    )


class AnnotationAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "id",
        "user",
        "highlight_start",
        "highlight_end",
        "created_on",
    )
    list_filter = ("article", "user", "is_public", "created_on")

    fields = [
        "id",
        "uuid",
        "created_on",
        "user",
        "article",
        "highlight_start",
        "highlight_end",
        "highlight_backward",
        "is_public",
    ]
    readonly_fields = ["id", "uuid", "created_on"]


class CommentAdmin(TreeAdmin):
    form = movenodeform_factory(Comment)
    list_display = ("comment_text", "uuid", "user")


admin.site.register(Article, ArticleAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Comment, CommentAdmin)
