# Generated by Django 4.2 on 2023-04-17 18:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_alter_commenttree_comment_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commenttree",
            name="created_on",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]