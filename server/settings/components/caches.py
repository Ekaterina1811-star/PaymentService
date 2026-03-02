# Caching
# https://docs.djangoproject.com/en/5.2/topics/cache/

CACHES = {
    'default': {
        # TODO: use some other cache in production,
        # like https://github.com/jazzband/django-redis
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
}


# django-axes
# https://django-axes.readthedocs.io/en/latest/4_configuration.html#configuring-caches

AXES_CACHE = 'default'

# Celery settings
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379"
