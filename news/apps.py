import redis
from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        pass


red = redis.Redis(
    host='redis-19964.c54.ap-northeast-1-2.ec2.cloud.redislabs.com',
    port=19964,
    password='Bzat4Uk9658aLlYLbjChc1Jxsvp7DWXa',
)
