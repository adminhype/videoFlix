from django.apps import AppConfig


class VideoAppConfig(AppConfig):
    """Configures the video application and registers signals on startup."""
    default_auto_field = "django.db.models.BigAutoField"
    name = 'video_app'

    def ready(self):
        import video_app.signals  # noqa
