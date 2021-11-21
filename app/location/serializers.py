import logging
from rest_framework import serializers
from .models import Location

logger = logging.getLogger(__name__)


class LocationSerializer(serializers.ModelSerializer):
    country_code = serializers.CharField()
    country = serializers.CharField()
    state = serializers.CharField()
    city = serializers.CharField()
    city_district = serializers.CharField()
    village = serializers.CharField()
    residential = serializers.CharField()
    postal_code = serializers.CharField()
    address = serializers.CharField()

    class Meta:
        model = Location
        fields = (
            "country_code",
            "country",
            "state",
            "city",
            "city_district",
            "village",
            "residential",
            "postal_code",
            "address",
        )
