from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ForumConfig(AppConfig):
    name = "app.forum"
    verbose_name = _("Forum")

    def ready(self):
        try:
            import aigis.forum.signals  # noqa F401
        except ImportError:
            pass
