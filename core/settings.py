from os import getenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = getenv("SECRET_KEY", "")
DEBUG = int(getenv("DEBUG", 1)) == 1

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = getenv("CSRF_TRUSTED_ORIGINS", "").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
]

APPLICATION_APPS = ["app"]

INSTALLED_APPS += APPLICATION_APPS

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_MIDDLEWARES = [
    "corsheaders.middleware.CorsMiddleware",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    *CORS_MIDDLEWARES,
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = []


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "django_style": {
            "format": "[%(asctime)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "django_style",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# Open Ai
OPENAI_API_KEY = getenv("OPENAI_API_KEY", "")

# Google
GOOGLE_API_KEY = getenv("GOOGLE_API_KEY", "")
GOOGLE_CX = getenv("GOOGLE_CX", "")

# Celery
CELERY_BROKER_URL = getenv("CELERY_BROKER_URL", "")

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# AWS
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = getenv("AWS_S3_REGION_NAME")
AWS_S3_ENDPOINT_URL = getenv("AWS_S3_ENDPOINT_URL")
AWS_DEFAULT_ACL = getenv("AWS_DEFAULT_ACL")
AWS_PRESIGNED_EXPIRE = getenv("AWS_PRESIGNED_EXPIRE")
