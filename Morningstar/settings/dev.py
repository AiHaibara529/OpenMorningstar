from .common import *

SECRET_KEY = 'django-insecure-o29$)y=p*bnwu!uqa8!@$w)l1gz#n@=%&&ze+xur%w)799)4%8'
DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'database/morningstar.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    "redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "1234asdw"
        }
    }
}

# 采用本地的静态文件
STATIC_URL = '/static/'


# RECAPTCHA-V2
RECAPTCHA_DOMAIN = 'www.recaptcha.net'
RECAPTCHA_PUBLIC_KEY = '6Le20wwdAAAAAKjy3eAJ8BPLN59KDRrRBeslsqpw'
RECAPTCHA_PRIVATE_KEY = '6Le20wwdAAAAAIyF33a5fiD-PJ7uioonJQ9ycilI'

# 添加测试环境的配置
try:
    from .test import *
except:
    pass