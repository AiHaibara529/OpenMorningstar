"""
Django settings for Morningstar project.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/

Quick-start development settings - unsuitable for production
See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
"""

import sys
from pathlib import Path
import os
import colorama
import logging

# 加载第三方配置文件
from .jazzmin import *
from .pure_pagination import *
from .haystack import *
# NOTE: 本项目的密钥保存方法如下
# 1. 开发与部署环境密钥相同时，开发密钥通过.env加载，部署密钥通过环境变量加载
# 2. 不相同时，开发密钥直接放入开发配置文件(dev.py)中，部署密钥仍通过环境变量加载
from dotenv import load_dotenv
env_path = os.getcwd() + "/.env"
load_dotenv(dotenv_path=env_path, verbose=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

AUTH_USER_MODEL = 'Morningstar.User'
ROOT_URLCONF = 'Morningstar.urls'
WSGI_APPLICATION = 'Morningstar.wsgi.application'


"""应用列表"""
INSTALLED_APPS = [
    'Morningstar.apps.BaseConfig',  # 基本

    'apps.album.apps.AlbumConfig',  # 相册
    'apps.blog.apps.BlogConfig',  # 博客
    'apps.book.apps.BookConfig',  # 书籍
    'apps.forum.apps.ForumConfig',  # 论坛
    'apps.nav.apps.NavConfig',  # 导航
    'apps.poll.apps.PollConfig',  # 投票
    'apps.shop.apps.ShopConfig',  # 商店
    'apps.v2ray.apps.V2RayConfig',  # 代理

    'jazzmin',  # UI定制
    'pure_pagination',  # 分页
    'haystack',  # 搜索
    'captcha',  # google recaptcha
    'django_user_agents',  # 获取客户端代理类型
    'rest_framework',  # restful api
    'django_filters',  # 过滤器
    'import_export',  # 导入导出
    'corsheaders',  # 处理跨域访问
    'debug_toolbar',  # 调试工具
    'django_crontab', # 定时任务
    "compressor", # 压缩js/css

    'django.contrib.humanize',  # {% load humanize %}
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',  # 站点地图
    # NOTE: 相当于在url中添加static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    'django.contrib.staticfiles',
]


"""中间价"""
MIDDLEWARE = [
    # The order of MIDDLEWARE is important. You should include the Debug Toolbar middleware as early as possible in the list. However, it must come after any other middleware that encodes the response’s content, such as GZipMiddleware
    "debug_toolbar.middleware.DebugToolbarMiddleware",

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # NOTE: 位置固定；
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',  # 404邮箱提醒

    'Morningstar.middleware.maintenance.MaintenanceMiddleware', # 维护中的站点重定向

]


"""跨域访问"""
CORS_ALLOWED_ORIGINS = [
    "https://morningstar529.com",
    "http://localhost:8000",  # NOTE: 测试专用
]
# CORS_ALLOW_ALL_ORIGINS = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [  # BASE_DIR / 'templates', 减少根目录文件夹数量?
            os.path.join(BASE_DIR, 'Morningstar', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django.templatetags.static',  # NOTE: 默认在模版中启用{%load static %}
            ],
        },
    },
]


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-Hans'

# datetime.datetime.now() - 东八区时间 / datetime.datetime.utcnow() => utc时间
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True
# USE_L10N = True  # NOET: Django5.0起, 此设置移除

# USE_TZ = True # NOTE: 使用的是UTC时间
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # 收集静态
STATICFILES_DIRS = [  # NOTE: 除app/static/外的静态文件
    # os.path.join(BASE_DIR, 'Morningstar', 'static')
    BASE_DIR / 'Morningstar' / 'static'
]


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


"""邮件"""
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'morningstar1.gcp@gmail.com'
try:
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
except KeyError:
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'morningstar1.gcp@gmail.com'
SERVER_EMAIL = 'morningstar1.gcp@gmail.com'
# 500
ADMINS = [('Henry', 'admin@morningstar529.com')]
# ADMINS = [('Ai', 'morningstar1.gcp@gmail.com')]
# 404
MANAGERS = [('Henry', 'admin@morningstar529.com')]
# MANAGERS = [('Ai', 'morningstar1.gcp@gmail.com')]


"""腾讯云短信"""
TENCENT_SMS_APP_ID = 1400623801
try:
    TENCENT_SMS_APP_KEY = os.environ['TENCENT_SMS_APP_KEY']
except KeyError:
    TENCENT_SMS_APP_KEY = os.getenv(key="TENCENT_SMS_APP_KEY")
TENCENT_SMS_SIGN = "嘉鱼居个人公众号"

TENCENT_SMS_TEMPLATE = {
    'register': 1278655,
    'login': 1278656,
    'chpasswd': 1278679,
}

"""用户数据存储(七牛云)"""
QINIU_ACCESS_KEY = 'LMsUR-Uiadd1ROKIM_xxyCwujI2Nl8UC7C6ltKd_'
try:  # NOTE: 环境变量优先级高于配置文件
    QINIU_SECRET_KEY = os.environ['QINIU_SECRET_KEY']
except KeyError:
    QINIU_SECRET_KEY = os.getenv(key="QINIU_SECRET_KEY")
QINIU_BUCKET_NAME = 'morningstar-529'
QINIU_BUCKET_DOMAIN = 'cdn.morningstar529.com'
PREFIX_URL = 'https://'
MEDIA_URL = PREFIX_URL + QINIU_BUCKET_DOMAIN + '/media/'
# MEDIA_URL = "/media/"  # 本地存储用户数据

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuMediaStorage'


"""日志系统"""
# https://docs.djangoproject.com/zh-hans/3.2/topics/logging/
# 原版: https://github.com/django/django/blob/main/django/utils/log.py


class HttpHostFilter(logging.Filter):
    BANNED_HTTP_HOST = ["www2.vitaminshub.com.au",
                        "azenv.net", "0.0.0.0:8000", "www"]

    def filter(self, record):
        http_host = request.META.get('HTTP_HOST')
        if http_host in BANNED_HTTP_HOST:
            return False
        else:
            return True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname}: {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
            "datefmt": "%m/%d/%Y %H:%M:%S %p"
        },
        'simple': {
            'format': colorama.Fore.YELLOW + colorama.Style.BRIGHT + '{levelname}: {message}' + colorama.Style.RESET_ALL,
            'style': '{',
            "datefmt": "%m/%d/%Y %H:%M:%S %p"
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'http_host_filter': {
            '()': HttpHostFilter,
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false', 'http_host_filter'],
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {  # 将所有信息传递给 console 处理程序
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}


"""Debug Toolbar"""
INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    # 'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    # 'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    # 'debug_toolbar.panels.profiling.ProfilingPanel',
]

"""定时任务"""
CRONJOBS =  [
    ("0 0 * * *", "Morningstar.cron.test", ">> " + str(BASE_DIR) + "/log/cron.log")
]

"""压缩js/css"""
COMPRESS_ROOT = os.path.join(BASE_DIR, "static")
COMPRESS_ENABLED = True
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'compressor.finders.CompressorFinder')