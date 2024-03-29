# Generated by Django 4.2 on 2023-04-10 16:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_annotation_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="annotation",
            name="uuid",
            field=models.UUIDField(db_index=True, default=uuid.uuid4, unique=True),
        ),
    ]
