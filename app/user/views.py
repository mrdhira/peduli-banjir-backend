import logging
from rest_framework import permissions
from rest_framework.views import APIView
from app.utils.http import generic_get, generic_post
from .models import User
from .serializers import (
    PassSerializer,
    LoginRequestSerializer,
    LoginResponseSerializer,
    ProfileSerializer,
    GenerateTokenSerializer,
)

logger = logging.getLogger(__name__)

# Create your views here.
class LoginView(APIView):
    def post(self, request):
        return generic_post(
            request=request,
            create_method=User.objects.login,
            request_serializer=LoginRequestSerializer,
            response_serializer=LoginResponseSerializer,
        )


class ProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return generic_get(
            request=request,
            model_method=User.objects.get_profile,
            request_serializer=PassSerializer,
            response_serializer=ProfileSerializer,
            protected=True,
        )


class GenerateTokenView(APIView):
    def post(self, request):
        return generic_post(
            request=request,
            create_method=User.objects.generate_token,
            request_serializer=GenerateTokenSerializer,
            response_serializer=LoginResponseSerializer,
        )
