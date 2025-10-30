from django.apps import AppConfig


class MixinAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mixin_app'
