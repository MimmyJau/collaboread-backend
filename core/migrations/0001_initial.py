# Generated by Django 4.1.7 on 2023-03-14 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                ("title", models.CharField(max_length=1000)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "article_html",
                    models.TextField(
                        help_text="HTML / rich-text from rich-text editor."
                    ),
                ),
                (
                    "article_json",
                    models.JSONField(
                        help_text="JSON output from tiptap / ProseMirror."
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(help_text="If true, others can read it."),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Annotation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "highlight",
                    models.CharField(
                        help_text="Serialized range by Rangy library", max_length=200
                    ),
                ),
                (
                    "comment_html",
                    models.TextField(
                        blank=True, help_text="HTML / rich-text from rich-text editor."
                    ),
                ),
                (
                    "comment_json",
                    models.JSONField(
                        blank=True, help_text="JSON output from tiptap / ProseMirror."
                    ),
                ),
                (
                    "is_public",
                    models.BooleanField(help_text="If true, others can read it."),
                ),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.article"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
