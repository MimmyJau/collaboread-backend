# Generated by Django 4.2 on 2023-05-15 16:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_alter_annotation_article_alter_comment_article"),
    ]

    operations = [
        migrations.AddField(
            model_name="articlemp",
            name="author",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]