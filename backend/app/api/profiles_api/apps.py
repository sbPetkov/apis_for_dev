from django.apps import AppConfig


class ProfilesApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.profiles_api'

    def ready(self):
        import api.profiles_api.signals
