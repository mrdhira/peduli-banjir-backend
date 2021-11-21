from .base import *
from .base import env
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", True)

# Cors
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = env.list(
    "DJANG_CORS_ALLOWED_ORIGINS",
    default=[],  # Frontend url
)

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


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
# Digital Ocean Spaces
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/static/"

# MEDIA
PUBLIC_MEDIA_LOCATION = "media"
DEFAULT_FILE_STORAGE = "app.utils.storages.PublicMediaStorage"
MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/media/"
# private media settings
PRIVATE_MEDIA_LOCATION = "private"
PRIVATE_FILE_STORAGE = "app.utils.storages.PrivateMediaStorage"
