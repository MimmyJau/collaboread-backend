from django.contrib import admin
from .models import Article, Annotation, Comment


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


class AnnotationAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "id",
        "user",
        "highlight_start",
        "highlight_end",
        "created_on",
    )
    list_filter = ("article", "user", "created_on")

    fields = [
        "id",
        "uuid",
        "created_on",
        "user",
        "article",
        "highlight_start",
        "highlight_end",
        "highlight_backward",
    ]
    readonly_fields = ["id", "uuid", "created_on"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ("annotation", "user", "created_on")
    list_filter = ("annotation", "user", "created_on")

    fields = [
        "id",
        "uuid",
        "created_on",
        "user",
        "annotation",
        "parent",
        "comment_html",
        "comment_json",
    ]
    readonly_fields = ["id", "uuid", "created_on"]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Comment, CommentAdmin)
