# Generated by Django 4.2 on 2023-05-30 18:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0012_rename_highlight_serialized_annotation_highlight_serialization"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="annotation",
            name="highlight_serialization",
        ),
    ]
