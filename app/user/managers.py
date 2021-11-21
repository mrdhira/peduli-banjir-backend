import logging
import requests
import io
from django.conf import settings
from django.contrib.auth.models import UserManager
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from google.oauth2 import id_token

logger = logging.getLogger(__name__)


def google_verify_oauth2(access_token):
    from google.auth.transport import requests
    from .serializers import GoogleOauth2Serializer

    GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID  # Get from env
    GOOGLE_ACCESS_TOKEN = access_token  # Get from payload

    try:
        result = id_token.verify_oauth2_token(
            GOOGLE_ACCESS_TOKEN,
            requests.Request(),
            GOOGLE_CLIENT_ID,
        )

        logger.info("result from google oauth2 token", result=result)
        serializer = GoogleOauth2Serializer(data=result)

        if serializer.is_valid():
            return serializer.data
        else:
            return serializer.error_messages
    except Exception as e:
        raise e


def jwt_token_generate(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    payload["roles"] = list(user.groups.values_list("name", flat=True))

    token = jwt_encode_handler(payload)
    return token


class UserCustomManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().order_by("full_name")

    def get_profile(self, fields):
        user = fields.get("user")

        logger.info("inside user authentication", user)

        return user

    def login(self, fields):
        access_token = fields.get("access_token")

        google_data = google_verify_oauth2(access_token)
        email = google_data["email"]

        user = self.filter(email=google_data["email"]).first()
        if not user:
            google_id = google_data["sub"]
            full_name = google_data["name"]
            email = google_data["email"]
            picture = google_data["picture"]

            username = email

            picture = requests.get(picture).content
            image_file = io.BytesIO()
            length = image_file.write(picture)
            display_picture = InMemoryUploadedFile(
                image_file, None, email + ".jpg", "image/jpeg", length, None
            )

            user = self.create(
                username=username,
                full_name=full_name,
                email=email,
                google_id=google_id,
                display_picture=display_picture,
            )
        if not user.google_id:
            google_id = google_data["sub"]
            picture = google_data["picture"]

            picture = requests.get(picture).content
            image_file = io.BytesIO()
            length = image_file.write(picture)
            display_picture = InMemoryUploadedFile(
                image_file, None, email + ".jpg", "image/jpeg", length, None
            )

            user.display_picture = display_picture
            user.google_id = google_id
            user.save()

        return user

    def generate_token(self, fields):
        email = fields.get("email")

        user = self.filter(email=email).first()

        if not user:
            raise ObjectDoesNotExist

        return user
