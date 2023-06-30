from django.apps import AppConfig

class SoccerboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "soccerboard"

    def ready(self):
        '''
        Start with fresh data model
        '''
        from soccerboard import schedule
        schedule

