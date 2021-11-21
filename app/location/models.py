from django.db import models

# from django.contrib.gis.db.models import PointField
# from django.contrib.gis.db import models
from .managers import LocationManager

# Create your models here.
class Location(models.Model):
    country_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255, blank=True, null=True)
    city_district = models.CharField(max_length=255, blank=True, null=True)
    village = models.CharField(max_length=255, blank=True, null=True)
    residential = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=5, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    objects = LocationManager()

    def __str__(self) -> str:
        return f"{self.id} - {self.country_code} - {self.country} - {self.state}"

    class Meta:
        db_table = "location"
        unique_together = (
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
