"""Django settings. Everything that differs between environments comes from env vars."""

import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-insecure-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,backend").split(",")

INSTALLED_APPS = [
    # daphne must come first: it replaces `runserver` with an ASGI server,
    # which is what lets the dev server handle WebSockets too.
    "daphne",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "rest_framework",
    "rest_framework.authtoken",  # DRF tokens, the same auth Tread's WebSocket accepts
    "channels",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"
ASGI_APPLICATION = "config.asgi.application"

# Postgres in Docker; SQLite when DATABASE_URL isn't set (quick local runs, tests).
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=60,
    )
}

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# The channel layer is how different processes talk to WebSocket connections.
# A message published to a group in Redis reaches every browser in that group,
# whichever backend process holds its socket.
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [REDIS_URL]},
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    # Only JSON responses; no browsable-API HTML.
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    # Decimals go out as strings ("0.10000000"), never floats. More in step 3.
    "COERCE_DECIMAL_TO_STRING": True,
}

USE_TZ = True
TIME_ZONE = "UTC"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
