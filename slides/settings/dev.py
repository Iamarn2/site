import json
import os

from .base import *  # noqa: F403, F401

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = "c6u0-9c!7nilj_ysatsda0(f@e_2mws2f!6m0n^o*4#*q#kzp)"

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

#Debug toolbar
INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
]

MIDDLEWARE = MIDDLEWARE + [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ("127.0.0.1", "172.17.0.1")

# WAGTAILADMIN_BASE_URL required for notification emails
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

ALLOWED_HOSTS = json.loads(os.environ['DJANGO_ALLOWED_HOSTS'])

RECAPTCHA_PUBLIC_KEY = os.getenv("WAGTAIL_RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.getenv("WAGTAIL_RECAPTCHA_PRIVATE_KEY")
NOCAPTCHA = True
SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#EMAIL_HOST = os.getenv("GOOGLE_EMAIL_HOST")
#EMAIL_USE_TLS = os.getenv("GOOGLE_EMAIL_USE_TLS")
#EMAIL_PORT = os.getenv("GOOGLE_EMAIL_PORT")
#EMAIL_HOST_USER = os.getenv("GOOGLE_EMAIL_HOST_USER")
#EMAIL_HOST_PASSWORD = os.getenv("GOOGLE_EMAIL_HOST_PASSWORD")
#DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
