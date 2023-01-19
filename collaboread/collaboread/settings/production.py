import dj_database_url

from collaboread.settings.base import *

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
"""
