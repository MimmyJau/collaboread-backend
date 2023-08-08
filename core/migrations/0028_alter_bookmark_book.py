# Generated by Django 4.2 on 2023-07-04 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0027_bookmark_book_alter_bookmark_article"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookmark",
            name="book",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="core.article",
            ),
            preserve_default=False,
        ),
    ]