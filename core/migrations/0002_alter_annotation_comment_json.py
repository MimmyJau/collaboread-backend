# Generated by Django 4.1.7 on 2023-03-14 18:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="annotation",
            name="comment_json",
            field=models.JSONField(
                blank=True,
                help_text="JSON output from tiptap / ProseMirror.",
                null=True,
            ),
        ),
    ]