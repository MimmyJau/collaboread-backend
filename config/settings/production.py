import dj_database_url

from config.settings.base import *


DEBUG = False

ALLOWED_HOSTS = [
    "collaboread.herokuapp.com",
]

# For djangorestframework-cors-headers
CORS_ALLOWED_ORIGINS = ["https://collaboread-frontend.vercel.app"]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {}
DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)
