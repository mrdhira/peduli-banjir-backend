from django.db import models
from app.location.models import Location
from app.weather.managers import WeatherCurrentManager, WeatherForecastManager

# Create your models here.
class WeatherDesc(models.Model):
    openweather_id = models.IntegerField()
    main = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.main

    class Meta:
        db_table = "weather_desc"


class WeatherCurrent(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="weather_current",
    )
    weather_desc = models.ForeignKey(
        WeatherDesc,
        on_delete=models.CASCADE,
        related_name="weather_current",
    )
    timezone = models.IntegerField()  # Shift in seconds from UTC
    dt = models.BigIntegerField()  #  Current time, Unix, UTC
    sunrise = models.BigIntegerField()  # Sunrise time, Unix, UTC
    sunset = models.BigIntegerField()  # Sunset time, Unix, UTC
    temp = (
        models.FloatField()
    )  # Temperature. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
    temp_min = (
        models.FloatField()
    )  # Minimum temperature at the moment. This is minimal currently observed temperature (within large megalopolises and urban areas). Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
    temp_max = (
        models.FloatField()
    )  # Maximum temperature at the moment. This is maximal currently observed temperature (within large megalopolises and urban areas). Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
    feels_like = (
        models.FloatField()
    )  # Temperature. This temperature parameter accounts for the human perception of weather. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
    pressure = (
        models.IntegerField()
    )  # Atmospheric pressure (on the sea level, if there is no sea_level or grnd_level data), hPa
    humidity = models.IntegerField()  # Humidity, %
    clouds = models.IntegerField()  # Cloudiness, %
    visibility = models.IntegerField()  # Average visibility, metres
    wind_speed = (
        models.FloatField()
    )  # Wind speed. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour.
    wind_deg = models.IntegerField()  # Wind direction, degrees (meteorological)
    wind_gust = (
        models.FloatField()
    )  # Wind gust. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour
    rain_1h = models.FloatField()  # Rain volume for the last 1 hour, mm
    rain_3h = models.FloatField()  # Rain volume for the last 3 hour, mm
    sea_level = models.IntegerField()  # Atmospheric pressure on the sea level, hPa
    ground_level = (
        models.IntegerField()
    )  # Atmospheric pressure on the ground level, hPa
    object = WeatherCurrentManager()

    class Meta:
        db_table = "weather_current"


class WeatherForecast(models.Model):
    class ForecastType(models.IntegerChoices):
        CURRENT = 1, "Current"
        MINUTELY = 2, "Minutely"
        HOURLY = 3, "Hourly"
        DAILY = 4, "Daily"

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="weather_forecast",
    )
    weather_desc = models.ForeignKey(
        WeatherDesc,
        on_delete=models.CASCADE,
        related_name="weather_forecast",
    )
    timezone = models.CharField(
        max_length=255
    )  # Timezone name for the requested location
    timezone_offset = models.IntegerField()  # Shift in seconds from UTC
    dt = models.BigIntegerField()  # Current, Hourly, Daily ->  Current time, Unix, UTC
    sunrise = models.BigIntegerField()  # Current, Daily -> Sunrise time, Unix, UTC
    sunset = models.BigIntegerField()  # Current, Daily -> Sunset time, Unix, UTC
    moonrise = (
        models.BigIntegerField()
    )  # Daily ->  The time of when the moon rises for this day, Unix, UTC
    moonset = (
        models.BigIntegerField()
    )  # Daily -> The time of when the moon sets for this day, Unix, UTC
    moon_phase = (
        models.FloatField()
    )  # Daily -> Moon phase. 0 and 1 are 'new moon', 0.25 is 'first quarter moon', 0.5 is 'full moon' and 0.75 is 'last quarter moon'. The periods in between are called 'waxing crescent', 'waxing gibous', 'waning gibous', and 'waning crescent', respectively.
    temp = (
        models.FloatField()
    )  # Current, Hourly -> Temperature. Units - default: kelvin, metric: Celsius, imperial: Fahrenheit.
    temp_min = models.FloatField()  # Daily -> Min daily temperature.
    temp_max = models.FloatField()  # Daily -> Max daily temperature.
    temp_morn = models.FloatField()  # Daily -> Morning temperature.
    temp_day = models.FloatField()  # Daily -> Day temperature.
    temp_eve = models.FloatField()  # Daily -> Evening temperature.
    temp_night = models.FloatField()  # Daily -> Night temperature.
    feels_like = (
        models.FloatField()
    )  # Current, Hourly -> Temperature. This temperature parameter accounts for the human perception of weather. Units – default: kelvin, metric: Celsius, imperial: Fahrenheit.
    feels_like_morn = models.FloatField()  # Daily ->  Morning temperature.
    feels_like_day = models.FloatField()  # Daily ->  Day temperature.
    feels_like_eve = models.FloatField()  # Daily ->  Evening temperature.
    feels_like_night = models.FloatField()  # Daily ->  Night temperature.
    pressure = (
        models.IntegerField()
    )  # Current, Hourly, Daily -> Atmospheric pressure on the sea level, hPa
    humidity = models.IntegerField()  # Current, Hourly, Daily -> Humidity, %
    dew_point = (
        models.FloatField()
    )  # Current, Hourly, Daily -> Atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to condense and dew can form. Units – default: kelvin, metric: Celsius, imperial: Fahrenheit.
    uvi = models.FloatField()  # Current, Hourly, Daily -> Current UV index
    clouds = models.IntegerField()  # Current, Hourly, Daily -> Cloudiness, %
    visibility = models.IntegerField()  # Current, Hourly -> Average visibility, metres
    wind_speed = (
        models.FloatField()
    )  # Current, Hourly, Daily ->  Wind speed. Units – default: metre/sec, metric: metre/sec, imperial: miles/hour.
    wind_deg = (
        models.IntegerField()
    )  # Current, Hourly, Daily ->  Wind direction, degrees (meteorological)
    wind_gust = (
        models.FloatField()
    )  # Current, Hourly, Daily ->  Wind gust. Units – default: metre/sec, metric: metre/sec, imperial: miles/hour.
    rain = models.FloatField()  # Daily -> Precipitation volume, mm
    rain_1h = models.FloatField()  # Current, Hourly -> Rain volume for last hour, mm
    precipitation = models.IntegerField()  # Minutely -> Precipitation volume, mm
    pop = models.IntegerField()  # Hourly, Daily -> Probability of precipitation
    type = models.IntegerField(choices=ForecastType.choices)
    object = WeatherForecastManager()

    def __str__(self) -> str:
        return f"{self.type} - {self.dt}"

    class Meta:
        db_table = "weather_forecast"
