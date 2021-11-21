from django.db import models
from app.user.models import User
from app.location.models import Location
from .managers import AlertManager

# Create your models here.
class Alert(models.Model):
    class AlertStatus(models.IntegerChoices):
        REPORTED = 1, "Reported"
        SOLVED = 2, "Solved"

    class FloodStatus(models.IntegerChoices):
        SAFE = 1, "Safe"
        WARNING = 2, "Warning"
        DANGER = 3, "Danger"

    user_report = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="alert",
        blank=True,
        null=True,
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="location_lat_long_mapping"
    )
    latitude = models.FloatField(
        blank=True,
        null=True,
    )
    longtitude = models.FloatField(
        blank=True,
        null=True,
    )
    status = models.IntegerField(
        choices=AlertStatus.choices,
        default=AlertStatus.REPORTED,
    )
    flood_status = models.IntegerField(
        choices=FloodStatus.choices,
        default=FloodStatus.SAFE,
    )
    flood_depth = models.FloatField(
        blank=True,
        null=True,
    )
    is_user_report = models.BooleanField(default=False)
    is_system_report = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    objects = AlertManager()

    class Meta:
        db_table = "alert"
