from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WeatherConfig(AppConfig):
    name = "app.weather"
    verbose_name = _("Weather")

    def ready(self):
        try:
            import aigis.weather.signals  # noqa F401
        except ImportError:
            pass
