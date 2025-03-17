from django.apps import AppConfig


class DwitterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dwitter"

    def ready(self):
        import dwitter.signals # import signals module