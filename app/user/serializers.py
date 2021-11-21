from django.db import models
from rest_framework import serializers
from .models import User


class GoogleOauth2Serializer(serializers.Serializer):
    id = serializers.CharField(source="result.sub")
    email = serializers.CharField(source="result.email")
    name = serializers.CharField(source="result.name")
    picture = serializers.CharField(source="result.picture")


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(source="user.username")
    email = serializers.CharField(source="user.email")


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    full_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    gender = serializers.CharField()
    display_picture = serializers.SerializerMethodField()

    def get_display_picture(self, obj):
        return obj.display_picture.url

    class Meta:
        models = User
        fields = "__all__"
