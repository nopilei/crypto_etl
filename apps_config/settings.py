import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'daphne',
    'channels',

    'apps.polygon.apps.PolygonConfig',

]

MIDDLEWARE = []
ROOT_URLCONF = 'apps_config.urls'

WSGI_APPLICATION = 'apps_config.wsgi.application'
ASGI_APPLICATION = 'apps_config.asgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        'apps': {
            'handlers': ['console'],
            'formatters': ['default'],
            'level': 'DEBUG'
        },
        'websockets': {
            'level': 'CRITICAL',
        }
    }
}
