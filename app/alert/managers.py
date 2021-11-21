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
        from .models import Alert

        latitude = fields.get("latitude")
        longtitude = fields.get("longtitude")

        location = Location.objects.get_location(latitude, longtitude)

        print("===========")
        print(location)
        print("===========")

        alert = self.filter(
            Q(flood_status=Alert.FloodStatus.WARNING)
            or Q(flood_status=Alert.FloodStatus.DANGER),
            status=Alert.AlertStatus.REPORTED,
            location=location,
        )

        print("===========")
        print(alert.all())
        print("===========")

        return alert

    def get_alert_by_latlong_city_district_group(self, fields):
        from .models import Alert

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

    def crete_alert(self, user, location, latitude, longtitude):
        from .models import Alert

        return self.create(
            user_report=user,
            location=location,
            latitude=latitude,
            longtitude=longtitude,
            flood_status=Alert.FloodStatus.WARNING,
            is_user_report=True,
        )
