from django_redis import get_redis_connection
from django.core.cache import cache

try:
    redis_client = get_redis_connection()
except Exception as e:
    redis_client = cache
