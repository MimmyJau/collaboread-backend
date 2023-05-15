from django.contrib import admin
from .models import Article, ArticleMP, Annotation, Comment

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "uuid", "user", "created_on")
    list_filter = ("user", "created_on")

    fields = [
        "id",
        "uuid",
        "created_on",
        "user",
        "title",
        "article_html",
        "article_json",
        "is_published",
    ]
    readonly_fields = ["id", "uuid", "created_on"]


class ArticleMPAdmin(TreeAdmin):
    form = movenodeform_factory(ArticleMP)
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
                    "user",
                    "title",
                    "author",
                    "article_html",
                    "article_json",
                    "article_text",
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


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleMP, ArticleMPAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Comment, CommentAdmin)
