import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        super().create_user(
            username=email, email=email, password=password, **extra_fields
        )

    def create_superuser(self, email, password=None, **extra_fields):
        super().create_superuser(
            username=email, email=email, password=password, **extra_fields
        )


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

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
