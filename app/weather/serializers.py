import logging
from rest_framework import serializers
from .models import WeatherCurrent, WeatherForecast

logger = logging.getLogger(__name__)


class WeatherQueryParamsSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required=True)
    longtitude = serializers.FloatField(required=True)


class WeatherCurrentSerializer(serializers.ModelSerializer):
    # Location
    location_state = serializers.CharField(source="location.state")
    location_city = serializers.CharField(source="location.city")
    location_address = serializers.CharField(source="location.address")
    # Weather Description
    weather_main = serializers.CharField(source="weather_desc.main")
    weather_description = serializers.CharField(source="weather_desc.description")
    weather_icon = serializers.CharField(source="weather_desc.icon")
    # Temperature
    temp = serializers.FloatField()
    temp_min = serializers.FloatField()
    temp_max = serializers.FloatField()
    feels_like = serializers.FloatField()
    humidity = serializers.IntegerField()
    datetime = serializers.SerializerMethodField()

    def get_datetime(self, obj):
        from datetime import datetime
        from django.utils.timezone import make_aware

        return make_aware(datetime.fromtimestamp(obj.dt))

    class Meta:
        model = WeatherCurrent
        fields = "__all__"


class WeatherForecastSerializer(serializers.ModelSerializer):
    # Location
    location_state = serializers.CharField(source="location.state")
    location_city = serializers.CharField(source="location.city")
    location_address = serializers.CharField(source="location.address")
    # Weather Description
    weather_main = serializers.CharField(source="weather_desc.main")
    weather_description = serializers.CharField(source="weather_desc.description")
    weather_icon = serializers.CharField(source="weather_desc.icon")
    # Temperature
    temp = serializers.FloatField()
    temp_min = serializers.FloatField()
    temp_max = serializers.FloatField()
    feels_like = serializers.FloatField()
    humidity = serializers.IntegerField()
    datetime = serializers.SerializerMethodField()

    def get_datetime(self, obj):
        from datetime import datetime
        from django.utils.timezone import make_aware

        return make_aware(datetime.fromtimestamp(obj.dt))

    class Meta:
        model = WeatherForecast
        fields = "__all__"
