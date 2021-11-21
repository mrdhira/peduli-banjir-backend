import nested_admin
from django.contrib import admin

# Register your models here.
from .models import WeatherDesc, WeatherCurrent, WeatherForecast


class WeatherDescAdmin(admin.ModelAdmin):
    search_fields = (
        "main",
        "description",
    )


class WeatherCurrentAdmin(admin.ModelAdmin):
    list_display = (
        "location_address",
        "weather_desc_main",
        "weather_desc_description",
        "timezone",
        "datetime",
        "temp",
        "feels_like",
        "humidity",
        "visibility",
        "clouds",
    )

    search_fields = ("location__address",)

    list_filter = (
        "location__address",
        "weather_desc__main",
    )

    raw_id_admin = (
        "location",
        "weather_desc",
    )

    def location_address(self, obj):
        return obj.location.address

    location_address.short_description = "Location Address"
    location_address.admin_order_field = "location__address"

    def weather_desc_main(self, obj):
        return obj.location.address

    weather_desc_main.short_description = "Weather Desc - Main"
    weather_desc_main.admin_order_field = "weather_desc__main"

    def weather_desc_description(self, obj):
        return obj.location.address

    weather_desc_description.short_description = "Weather Desc - Description"
    weather_desc_description.admin_order_field = "weather_desc__description"

    def datetime(self, obj):
        from datetime import datetime
        from django.utils.timezone import make_aware

        return make_aware(datetime.fromtimestamp(obj.dt))


class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = (
        "location_address",
        "weather_desc_main",
        "weather_desc_description",
        "timezone",
        "timezone_offset",
        "datetime",
        "temp",
        "feels_like",
        "humidity",
        "visibility",
        "clouds",
    )

    def location_address(self, obj):
        return obj.location.address

    location_address.short_description = "Location Address"
    location_address.admin_order_field = "location__address"

    def weather_desc_main(self, obj):
        return obj.location.address

    weather_desc_main.short_description = "Weather Desc - Main"
    weather_desc_main.admin_order_field = "weather_desc__main"

    def weather_desc_description(self, obj):
        return obj.location.address

    weather_desc_description.short_description = "Weather Desc - Description"
    weather_desc_description.admin_order_field = "weather_desc__description"

    def datetime(self, obj):
        from datetime import datetime
        from django.utils.timezone import make_aware

        return make_aware(datetime.fromtimestamp(obj.dt))


admin.site.register(WeatherDesc, WeatherDescAdmin)
admin.site.register(WeatherCurrent, WeatherCurrentAdmin)
admin.site.register(WeatherForecast, WeatherForecastAdmin)
