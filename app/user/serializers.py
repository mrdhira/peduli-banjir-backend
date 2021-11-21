import logging
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import User

logger = logging.getLogger(__name__)


def jwt_token_generate(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    payload["roles"] = list(user.groups.values_list("name", flat=True))

    token = jwt_encode_handler(payload)
    return token


class PassSerializer:
    def __init__(self, data, *args, **kwargs):
        self.data = data

    def is_valid(self):
        return True


class GoogleOauth2Serializer(serializers.Serializer):
    sub = serializers.CharField()
    email = serializers.CharField()
    name = serializers.CharField()
    picture = serializers.CharField()


class LoginRequestSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)


class LoginResponseSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    exp = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    def get_user(self, obj):
        return ProfileSerializer(obj).data

    def get_token(self, obj):
        token = jwt_token_generate(obj)
        return token

    def get_exp(self, obj):
        token = self.get_token(obj)
        token_info = api_settings.JWT_DECODE_HANDLER(token)

        logger.info("token info", token_info)

        return token_info.get("exp")


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    full_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    gender = serializers.CharField()
    display_picture = serializers.SerializerMethodField()

    def get_display_picture(self, obj):
        return obj.get_display_picture()

    class Meta:
        model = User
        fields = (
            "username",
            "full_name",
            "email",
            "phone_number",
            "gender",
            "display_picture",
        )


class GenerateTokenSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
