from django.contrib import admin

# Register your models here.
from .models import Location


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "country_code",
        "country",
        "state",
        "city",
        "city_district",
        "village",
        "residential",
        "address",
    )

    search_fields = (
        "country_code",
        "country",
        "state",
        "city",
        "city_district",
        "village",
        "residential",
        "address",
    )

    list_filter = (
        "country_code",
        "country",
        "state",
    )


admin.site.register(Location, LocationAdmin)
