from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ("username", "uuid", "email", "is_staff")
    # Copied and pasted from ../django/contrib/auth/admin.py
    # Requires import gettext_lazy as _
    fieldsets = (
        (None, {"fields": ("username", "display_name", "email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"fields": ("username", "email", "password1", "password2")}),
    )


# Register your models here.
admin.site.register(User, UserAdmin)
