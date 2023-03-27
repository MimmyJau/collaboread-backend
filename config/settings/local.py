from config.settings.base import *

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "db",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# For djangorestframework-cors-headers
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]


# For django-debug-toolbars
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
INSTALLED_APPS.append("debug_toolbar")
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS = ["127.0.0.1"]
