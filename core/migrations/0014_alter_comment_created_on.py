# Generated by Django 4.2 on 2023-06-02 20:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_remove_annotation_highlight_serialization"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="created_on",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
