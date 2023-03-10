from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserCreationForm(forms.ModelForm):
    class Meta:
        fields = ("email", "password")


class UserAdmin(BaseUserAdmin):
    # add_form = UserCreationForm
    list_display = ("username", "name", "is_staff")
    # Copied and pasted from ../django/contrib/auth/admin.py
    # Requires import gettext_lazy as _
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
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


# Register your models here.
admin.site.register(User, UserAdmin)
