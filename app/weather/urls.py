from django.urls import path
from .views import WeatherCurrentView, WeatherForecastView

app_name = "weather"
urlpatterns = [
    path("current", view=WeatherCurrentView.as_view(), name="weather_current"),
    path("forecast", view=WeatherForecastView.as_view(), name="weather_forecast"),
]
