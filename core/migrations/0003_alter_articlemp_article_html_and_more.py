# Generated by Django 4.2 on 2023-05-03 17:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_articlemp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articlemp",
            name="article_html",
            field=models.TextField(
                blank=True, help_text="HTML output from WYSIWYG editor."
            ),
        ),
        migrations.AlterField(
            model_name="articlemp",
            name="article_json",
            field=models.JSONField(
                help_text="JSON output specific to ProseMirror.", null=True
            ),
        ),
        migrations.AlterField(
            model_name="articlemp",
            name="article_text",
            field=models.JSONField(
                blank=True, help_text="Text output from WYSIWYG editor."
            ),
        ),
    ]
