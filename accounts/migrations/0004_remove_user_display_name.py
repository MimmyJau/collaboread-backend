# Generated by Django 4.2 on 2023-06-19 22:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_user_custom_display_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="display_name",
        ),
    ]
