from django.apps import AppConfig


class CustomCommentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "slides.custom_comments"

    def ready(self):
        import slides.custom_comments.receivers
