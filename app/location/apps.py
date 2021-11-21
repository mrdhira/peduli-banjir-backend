from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LocationConfig(AppConfig):
    name = "app.location"
    verbose_name = _("Location")

    def ready(self):
        try:
            import aigis.location.signals  # noqa F401
        except ImportError:
            pass
