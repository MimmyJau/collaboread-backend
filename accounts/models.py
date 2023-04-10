import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    pass


class User(AbstractUser):
    """Custom User"""

    # Keep pk as auto-incrementing id for internal work.
    # Have uuid for external-facing.
    uuid = models.UUIDField(
        db_index=True, default=uuid.uuid4, editable=False, unique=True
    )
    email = models.EmailField(blank=False, default="", unique=True)
    name = models.CharField(max_length=200, blank=True, default="")

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
