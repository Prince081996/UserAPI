from Task.settings.base import *

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST':'127.0.0.1',
        'NAME': 'user_db',
        'PORT':5432,
        'USER':'prince',
        'PASSWORD':'prince@1996'
    }
}