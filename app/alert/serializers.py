import logging
from rest_framework import serializers
from app.location.serializers import LocationSerializer
from app.user.serializers import ProfileSerializer
from .models import Alert

logger = logging.getLogger(__name__)


class AlertByLatlongSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required=True)
    longtitude = serializers.FloatField(required=True)


class AlertSerializer(serializers.ModelSerializer):
    user_report = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    latitude = serializers.FloatField()
    longtitude = serializers.FloatField()
    status = serializers.IntegerField()
    flood_status = serializers.IntegerField()
    flood_depth = serializers.FloatField()
    is_user_report = serializers.BooleanField()
    is_system_report = serializers.BooleanField()

    def get_user_report(self, obj):
        return ProfileSerializer(obj.user_report).data

    def get_location(self, obj):
        return LocationSerializer(obj.location).data

    class Meta:
        model = Alert
        fields = (
            "user_report",
            "location",
            "latitude",
            "longtitude",
            "status",
            "flood_status",
            "flood_depth",
            "is_user_report",
            "is_system_report",
        )
