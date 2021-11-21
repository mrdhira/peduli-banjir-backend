from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    name = "app.user"
    verbose_name = _("User")

    def ready(self):
        try:
            import aigis.user.signals  # noqa F401
        except ImportError:
            pass
