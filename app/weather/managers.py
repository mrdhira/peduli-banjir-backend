import logging
import requests
from django.conf import settings
from django.db import transaction
from django.db.models import Manager
from app.location.models import Location

logger = logging.getLogger(__name__)


class WeatherCurrentManager(Manager):
    def get_current(self, fields):
        latitude = fields.get("latitude")
        longtitude = fields.get("longtitude")

        # Get from open weather
        query_params = {
            "appid": settings.OPEN_WEATHER_APP_ID,
            "lat": latitude,
            "lon": longtitude,
            "units": "imperial",
            "lang": "en",
        }
        curr_resp = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather",
            params=query_params,
        )

        logger.info(
            "request url to open weather api for get current weather",
            curr_resp.url,
        )

        weather_data = curr_resp.json()
        curr_resp.close()

        logger.info(
            "response from open weather api for get current weather", weather_data
        )

        # Weather Desc
        weather_desc_openweather_id = weather_data["weather"][0]["id"]
        weather_desc_main = weather_data["weather"][0]["id"]
        weather_desc_description = weather_data["weather"][0]["id"]
        weather_desc_icon = weather_data["weather"][0]["id"]

        # Weather Current
        timezone = weather_data.get("timezone", 0)
        dt = weather_data.get("dt", 0)
        sunrise = weather_data["sys"].get("sunrise", 0)
        sunset = weather_data["sys"].get("sunset", 0)
        temp = weather_data.get("", 0.0)
        temp_min = weather_data["main"].get("temp_min", 0.0)
        temp_max = weather_data["main"].get("temp_max", 0.0)
        feels_like = weather_data["main"].get("feels_like", 0.0)
        pressure = weather_data["main"].get("pressure", 0)
        humidity = weather_data["main"].get("humidity", 0)
        clouds = weather_data["clouds"].get("all", 0)
        visibility = weather_data.get("visibility", 0)
        wind_speed = weather_data["wind"].get("speed", 0.0)
        wind_deg = weather_data["wind"].get("deg", 0)
        wind_gust = weather_data["wind"].get("gust", 0.0)
        rain_1h = weather_data["rain"].get("1h", 0.0)
        rain_3h = weather_data["rain"].get("3h", 0.0)
        sea_level = weather_data["main"].get("sea_level", 0)
        ground_level = weather_data["main"].get("grnd_level", 0)

        from .models import WeatherDesc

        # Get Location
        with transaction.atomic():
            location = Location.objects.get_location(latitude, longtitude)

            weather_desc = WeatherDesc.objects.filter(
                openweather_id=weather_desc_openweather_id,
            ).first()

            if not weather_desc:
                weather_desc = WeatherDesc.objects.create(
                    openweather_id=weather_desc_openweather_id,
                    main=weather_desc_main,
                    description=weather_desc_description,
                    icon=weather_desc_icon,
                )

            # Insert to database
            weather_current = self.create(
                location,
                weather_desc,
                timezone,
                dt,
                sunrise,
                sunset,
                temp,
                temp_min,
                temp_max,
                feels_like,
                pressure,
                humidity,
                clouds,
                visibility,
                wind_speed,
                wind_deg,
                wind_gust,
                rain_1h,
                rain_3h,
                sea_level,
                ground_level,
            )

            return weather_current


class WeatherForecastManager(Manager):
    def get_forecast(self):
        return self.all()
