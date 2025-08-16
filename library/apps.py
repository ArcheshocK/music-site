from django.apps import AppConfig
from django.db.utils import OperationalError

class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'

    def ready(self):
        try:
            from django.contrib.auth.models import User

            SAMPLE_USERS = [
                ('alice', 'password123'),
                ('bob', 'password123'),
                ('axel', 'password123'),
            ]

            for username, password in SAMPLE_USERS:
                if not User.objects.filter(username=username).exists():
                    User.objects.create_user(username=username, password=password)

        except OperationalError:
            pass
