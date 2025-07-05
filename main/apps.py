from django.apps import AppConfig

class MainConfig(AppConfig):
    # Use BigAutoField by default for model primary keys
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"