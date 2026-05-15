"""
AfyaBoraHMIS — settings.py
Level 5 Hospital Management Information System
Django 4.x / 5.x compatible.

Usage:
  Set the environment variable DJANGO_ENV to 'production' in production.
  All sensitive values should come from environment variables or a .env file
  (use python-decouple or django-environ).
"""

import os
from pathlib import Path
from datetime import timedelta

# ──────────────────────────────────────────────────────────────
# BASE PATHS
# ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ──────────────────────────────────────────────────────────────
# ENVIRONMENT HELPERS
# Try to use python-decouple; fall back to os.environ.get
# ──────────────────────────────────────────────────────────────
try:
    from decouple import config, Csv
    def env(key, default=None, cast=str):
        return config(key, default=default, cast=cast)
except ImportError:
    def env(key, default=None, cast=str):
        value = os.environ.get(key, default)
        if value is None:
            return default
        return cast(value) if cast and cast != str else value

DJANGO_ENV = env('DJANGO_ENV', default='development')
IS_PRODUCTION = DJANGO_ENV == 'production'

# ──────────────────────────────────────────────────────────────
# SECURITY
# ──────────────────────────────────────────────────────────────
SECRET_KEY = env(
    'SECRET_KEY',
    default='django-insecure-change-me-in-production-use-a-long-random-string-here'
)

DEBUG = not IS_PRODUCTION

ALLOWED_HOSTS = env(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
).split(',') if IS_PRODUCTION else ['*']

# ──────────────────────────────────────────────────────────────
# APPLICATIONS
# ──────────────────────────────────────────────────────────────
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',
    # Uncomment when installed:
    # 'drf_spectacular',
    # 'channels',              # for WebSocket / real-time notifications
    # 'django_celery_beat',    # for periodic tasks
    # 'django_celery_results',
    # 'storages',              # for S3 / GCS file storage
]

LOCAL_APPS = [
    'core',     # ← rename to your actual app name (the one holding models.py)
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ──────────────────────────────────────────────────────────────
# MIDDLEWARE
# ──────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',            # must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ──────────────────────────────────────────────────────────────
# URLS & WSGI/ASGI
# ──────────────────────────────────────────────────────────────
ROOT_URLCONF = 'afyabora.urls'          # ← replace 'afyabora' with your project name

WSGI_APPLICATION = 'afyabora.wsgi.application'
# ASGI_APPLICATION = 'afyabora.asgi.application'   # enable when using Channels

# ──────────────────────────────────────────────────────────────
# TEMPLATES
# ──────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ──────────────────────────────────────────────────────────────
# DATABASE
# ──────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='afyabora_db'),
        'USER': env('DB_USER', default='postgres'),
        'PASSWORD': env('DB_PASSWORD', default='postgres'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 60 if IS_PRODUCTION else 0,
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# ──────────────────────────────────────────────────────────────
# CUSTOM AUTH USER MODEL
# ──────────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'core.User'    # ← replace 'core' with your actual app name

# ──────────────────────────────────────────────────────────────
# PASSWORD VALIDATION
# ──────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ──────────────────────────────────────────────────────────────
# INTERNATIONALISATION
# ──────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'        # EAT (UTC+3) — Kenya
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────────────────────
# STATIC & MEDIA FILES
# ──────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Production: use S3 / GCS (uncomment and configure django-storages)
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
# AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default='')
# AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='af-south-1')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ──────────────────────────────────────────────────────────────
# DJANGO REST FRAMEWORK
# ──────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    # Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',   # for browsable API
    ],

    # Permissions — require authentication by default
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,

    # Filtering
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

    # Throttling — prevents brute-force / abuse
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '2000/hour',
    },

    # Renderer — JSON only in production; add BrowsableAPIRenderer in dev
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ] + (['rest_framework.renderers.BrowsableAPIRenderer'] if not IS_PRODUCTION else []),

    # Exception handler
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',

    # Date/datetime format
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
}

# ──────────────────────────────────────────────────────────────
# SIMPLE JWT
# ──────────────────────────────────────────────────────────────
SIMPLE_JWT = {
    # Token lifetimes
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),        # shift-length token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    # Signing
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    # Header
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

    # Claims
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    # Custom token with extra claims (optional)
    # 'TOKEN_OBTAIN_SERIALIZER': 'core.serializers.CustomTokenObtainPairSerializer',
}

# ──────────────────────────────────────────────────────────────
# CORS (django-cors-headers)
# ──────────────────────────────────────────────────────────────
if IS_PRODUCTION:
    CORS_ALLOWED_ORIGINS = env(
        'CORS_ALLOWED_ORIGINS',
        default='https://afyabora.example.com',
    ).split(',')
    CORS_ALLOW_CREDENTIALS = True
else:
    CORS_ALLOW_ALL_ORIGINS = True   # development only

CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization',
    'content-type', 'dnt', 'origin', 'user-agent',
    'x-csrftoken', 'x-requested-with',
]

CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']

# ──────────────────────────────────────────────────────────────
# CSRF
# ──────────────────────────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = env(
    'CSRF_TRUSTED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000',
).split(',')

# ──────────────────────────────────────────────────────────────
# CACHE — Redis (preferred for production)
# ──────────────────────────────────────────────────────────────
REDIS_URL = env('REDIS_URL', default='redis://127.0.0.1:6379/0')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
        'KEY_PREFIX': 'afyabora',
        'TIMEOUT': 300,
    }
} if IS_PRODUCTION else {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Session store (use Redis in production for shared sessions across workers)
if IS_PRODUCTION:
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 28800          # 8 hours (one shift)
SESSION_COOKIE_SECURE = IS_PRODUCTION
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# ──────────────────────────────────────────────────────────────
# EMAIL
# ──────────────────────────────────────────────────────────────
if IS_PRODUCTION:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = int(env('EMAIL_PORT', default='587'))
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='AfyaBora HMIS <noreply@afyabora.co.ke>')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'AfyaBora HMIS <dev@localhost>'

# ──────────────────────────────────────────────────────────────
# CELERY (background tasks — uncomment when using)
# ──────────────────────────────────────────────────────────────
# CELERY_BROKER_URL = env('CELERY_BROKER_URL', default=REDIS_URL)
# CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default=REDIS_URL)
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# ──────────────────────────────────────────────────────────────
# CHANNELS (WebSockets for real-time queue / notifications)
# ──────────────────────────────────────────────────────────────
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {'hosts': [REDIS_URL]},
#     }
# }

# ──────────────────────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'},
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'afyabora.log',
            'maxBytes': 10 * 1024 * 1024,   # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
        'core': {                           # your app
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if not IS_PRODUCTION else 'INFO',
            'propagate': False,
        },
    },
}

# Ensure logs directory exists
(BASE_DIR / 'logs').mkdir(exist_ok=True)

# ──────────────────────────────────────────────────────────────
# PRODUCTION SECURITY SETTINGS
# ──────────────────────────────────────────────────────────────
if IS_PRODUCTION:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 31536000          # 1 year
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

# ──────────────────────────────────────────────────────────────
# FILE UPLOAD LIMITS
# ──────────────────────────────────────────────────────────────
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024     # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024     # 10 MB

# ──────────────────────────────────────────────────────────────
# DRF SPECTACULAR (API docs) — uncomment when drf-spectacular installed
# ──────────────────────────────────────────────────────────────
# SPECTACULAR_SETTINGS = {
#     'TITLE': 'AfyaBora HMIS API',
#     'DESCRIPTION': 'Level 5 Hospital Management Information System — REST API',
#     'VERSION': '1.0.0',
#     'SERVE_INCLUDE_SCHEMA': False,
#     'COMPONENT_SPLIT_REQUEST': True,
#     'SCHEMA_PATH_PREFIX': '/api/v1/',
# }

# ──────────────────────────────────────────────────────────────
# APP-SPECIFIC SETTINGS
# ──────────────────────────────────────────────────────────────

# Account lockout policy
MAX_FAILED_LOGIN_ATTEMPTS = 5
ACCOUNT_LOCKOUT_DURATION_MINUTES = 30

# Two-factor authentication
TFA_CODE_EXPIRY_MINUTES = 2

# eTIMS
ETIMS_API_BASE_URL = env('ETIMS_API_BASE_URL', default='https://etims-api.kra.go.ke/etims-api')
ETIMS_TEST_MODE = not IS_PRODUCTION

# SHA API
SHA_API_BASE_URL = env('SHA_API_BASE_URL', default='https://api.sha.go.ke')

# M-Pesa (Daraja API)
MPESA_CONSUMER_KEY = env('MPESA_CONSUMER_KEY', default='')
MPESA_CONSUMER_SECRET = env('MPESA_CONSUMER_SECRET', default='')
MPESA_SHORTCODE = env('MPESA_SHORTCODE', default='')
MPESA_PASSKEY = env('MPESA_PASSKEY', default='')
MPESA_CALLBACK_URL = env('MPESA_CALLBACK_URL', default='https://afyabora.example.com/api/v1/mpesa/callback/')
MPESA_ENV = env('MPESA_ENV', default='sandbox')    # 'sandbox' | 'production'

# ──────────────────────────────────────────────────────────────
# ADMINS (for error emails in production)
# ──────────────────────────────────────────────────────────────
ADMINS = [('AfyaBora Admin', env('ADMIN_EMAIL', default='admin@afyabora.co.ke'))]
SERVER_EMAIL = DEFAULT_FROM_EMAIL