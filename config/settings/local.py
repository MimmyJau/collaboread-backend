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
