from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AlertConfig(AppConfig):
    name = "app.alert"
    verbose_name = _("Alert")

    def ready(self):
        try:
            import aigis.alert.signals  # noqa F401
        except ImportError:
            pass
