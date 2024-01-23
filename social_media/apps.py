from django.apps import AppConfig


class SocialMediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_media'

    def ready(self) -> None:
        from .signals import create_profile
