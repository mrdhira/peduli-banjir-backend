from rest_framework.views import APIView
from app.utils.http import generic_get
from .models import WeatherCurrent, WeatherForecast
from .serializers import (
    WeatherQueryParamsSerializer,
    WeatherCurrentSerializer,
    WeatherForecastSerializer,
)

# Create your views here.


class WeatherCurrentView(APIView):
    # GET Weather Current
    def get(self, request):
        return generic_get(
            request=request,
            model_method=WeatherCurrent.objects.get_current,
            request_serializer=WeatherQueryParamsSerializer,
            response_serializer=WeatherCurrentSerializer,
            many=False,
        )


class WeatherForecastView(APIView):
    # GET Weather Forecast
    def get(self, request):
        return generic_get(
            request=request,
            model_method=WeatherForecast.objects.get_forecast,
            request_serializer=WeatherQueryParamsSerializer,
            response_serializer=WeatherForecastSerializer,
            many=True,
        )
