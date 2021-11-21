import logging
from django.db import transaction
from django.db.models import Manager, Q
from app.location.models import Location
from app.location.serializers import LocationSerializer

logger = logging.getLogger(__name__)


class AlertManager(Manager):
    def get_alert(self, fields):
        return self.all()

    def get_alert_by_latlong(self, fields):
        latitude = fields.get("latitude")
        longtitude = fields.get("longtitude")

        location = Location.objects.get_location(latitude, longtitude)

        from .models import Alert

        alert = self.filter(
            Q(status=Alert.AlertStatus.WARNING) or Q(status=Alert.AlertStatus.DANGER),
            location=location,
        ).all()

        return alert

    def get_alert_by_latlong_city_district_group(self, fields):
        latitude = fields.get("latitude")
        longtitude = fields.get("longtitude")

        location = Location.objects.get_location(latitude, longtitude)
        location_data = LocationSerializer(location).data

        alert = (
            self.filter(
                Q(status=Alert.AlertStatus.WARNING)
                or Q(status=Alert.AlertStatus.DANGER),
                location__city=location_data["city"],
            )
            .values(
                "location__city",
                "location__city_district",
                "location__village",
                "location__residential",
                "flood_status",
                "flood_depth",
            )
            .distinct()
        )

        logger.info(
            "query result for get_alert_by_latlong_city_district_group", alert.get()
        )

        return alert

    def get_alert_by_latlong_radius(self, fields):
        latitude = fields.get("latitude")
        longtitude = fields.get("longtitude")

        RADIUS = 500

        return
