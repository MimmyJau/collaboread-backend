import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Boilerplate taken from src for UserManager."""
        extra_fields.setdefault("display_name", username)  # New line of code
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self._create_user(username.lower(), email, password, **extra_fields)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Boilerplate taken from src for UserManager"""
        extra_fields.setdefault("display_name", username)  # New line of code
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        """
        Make username case-insensitive.
        Source: https://stackoverflow.com/a/33456271
        """
        return self.get(username__iexact=username)


class User(AbstractUser):
    """Custom User"""

    # Keep pk as auto-incrementing id for internal work.
    # Have uuid for external-facing.
    uuid = models.UUIDField(
        db_index=True, default=uuid.uuid4, editable=False, unique=True
    )
    email = models.EmailField(blank=False, default="", unique=True)
    display_name = models.CharField(
        blank=False, max_length=150, help_text=("Case-sensitive version of username")
    )
    name = models.CharField(max_length=200, blank=True, default="")

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
