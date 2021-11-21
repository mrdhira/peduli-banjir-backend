from .base import *
from .base import env
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

# Cors
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = env.list(
    "DJANG_CORS_ALLOWED_ORIGINS",
    default=[],  # Frontend url
)

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# STORAGES
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ["storages"]  # noqa F405
AWS_ACCESS_KEY_ID = env("DO_SPACES_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("DO_SPACES_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("DO_SPACES_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = "public-read"
AWS_S3_ENDPOINT_URL = env("DO_SPACES_S3_ENDPOINT_URL")
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = env("DO_SPACES_LOCATION")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/static/"

# MEDIA
# public media settings
PUBLIC_MEDIA_LOCATION = "media"
DEFAULT_FILE_STORAGE = "app.utils.storages.PublicMediaStorage"
MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/media/"
# private media settings
PRIVATE_MEDIA_LOCATION = "private"
PRIVATE_FILE_STORAGE = "app.utils.storages.PrivateMediaStorage"

# LOGGING
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "gunicorn": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": "./gunicorn.errors",
            "maxBytes": 1024 * 1024 * 100,  # 100 mb
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
        "gunicorn.errors": {
            "level": "DEBUG",
            "handlers": ["gunicorn"],
            "propagate": True,
        },
    },
}
