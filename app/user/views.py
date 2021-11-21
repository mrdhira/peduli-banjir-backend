import logging
import requests
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from google.oauth2 import id_token
from .models import User
from .serializers import GoogleOauth2Serializer, TokenSerializer, ProfileSerializer

logger = logging.getLogger(__name__)

# Create your views here.
def google_verify_oauth2(access_token):
    from google.oauth2 import id_token
    from google.auth.transport import requests

    GOOGLE_CLIENT_ID = ""  # Get from env
    GOOGLE_ACCESS_TOKEN = access_token  # Get from payload

    try:
        result = id_token.verify_oauth2_token(
            GOOGLE_ACCESS_TOKEN,
            requests.Request(),
            GOOGLE_CLIENT_ID,
        )

        logger.info("result from google oauth2 token", result)

        return GoogleOauth2Serializer(data=result)
    except Exception as e:
        raise e


class LoginView(APIView):
    def post(self, request):
        return


class ProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        token = TokenSerializer(request.user)
        try:
            user = ProfileSerializer(
                User.objects.get_by_username(token.username),
                many=False,
            )
            return Response(
                data={
                    "code": status.HTTP_200_OK,
                    "message": "OK",
                    "error": None,
                    "data": user,
                },
                status=status.HTTP_200_OK,
            )
        except ObjectDoesNotExist as error:
            return Response(
                data={
                    "code": status.HTTP_404_NOT_FOUND,
                    "message": "User not found",
                    "error": None,
                    "data": None,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return Response(
                data={
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Internal server error",
                    "error": "{0}: {1}".format(type(error).__name__, error.args),
                    "data": None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
