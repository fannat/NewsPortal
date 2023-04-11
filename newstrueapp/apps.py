from django.apps import AppConfig
import redis


class NewstrueappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newstrueapp'
    def ready(self):
        import newstrueapp.signals

red = redis.Redis(
    host = 'redis-15251.c261.us-east-1-4.ec2.cloud.redislabs.com',
    port = 15251,
    password = 'JY9OVRfMU1gEB6TZijUgq5SD4BmKWGk6',
)
