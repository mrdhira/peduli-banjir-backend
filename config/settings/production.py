from .base import *
from .base import env
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

# Cors
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = env.list(
    "DJANG_CORS_ALLOWED_ORIGINS",
    default=[], # Frontend url
)

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# STORAGES
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ["storages"]  # noqa F405
GS_BUCKET_NAME = env("DJANGO_GCP_STORAGE_BUCKET_NAME")
GS_DEFAULT_ACL = "publicRead"

# STATIC
STATICFILES_STORAGE = "aigis.utils.storages.StaticRootGoogleCloudStorage"
COLLECTFAST_STRATEGY = "collectfast.strategies.gcloud.GoogleCloudStrategy"
STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"

# MEDIA
DEFAULT_FILE_STORAGE = "aigis.utils.storages.MediaRootGoogleCloudStorage"
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"

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