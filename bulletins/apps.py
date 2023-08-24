from django.apps import AppConfig


class BulletinsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bulletins'

    def ready(self):
        import bulletins.signals
