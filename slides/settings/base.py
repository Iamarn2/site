import os
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(PROJECT_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = False


# Uncomment this (and adjust as appropriate) to enable django-debug-toolbar
# INTERNAL_IPS = [
#     '127.0.0.1',
# ]

#    "wagtail.locales",заменила на wagtail_localize.locales
#    'wagtailvideos',
# Application definition
#    "slides.userauth",
#    "wagtailmenus",
#    "modeltranslation",
#     'wagtailmarkdown',
INSTALLED_APPS = [
    "slides.blog",
    "slides.base",
    "slides.wagtail_simple_gallery",
    "slides.custom_comments",
    "wagtail.contrib.search_promotions",
    "wagtail.locales",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.api.v2",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.simple_translation",
    "wagtail.contrib.styleguide",
    "wagtail",
    "wagtailfontawesome",
    "wagtailcaptcha",
    "wagtailmetadata",
    "rest_framework",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django_comments",
    "django.contrib.sites",
    "corsheaders",
    "crispy_forms",
    "crispy_bootstrap5",
    "crispy_tailwind",
    "captcha",
    "django_countries",
    "slides.userauth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "widget_tweaks",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.linkedin_oauth2",
    "wagtail.contrib.settings",


]

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.contrib.postgres_search.backend",
    }
}
# 'django.middleware.locale.LocaleMiddleware',
#    'wagtail.core.middleware.SiteMiddleware',
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",

]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
ROOT_URLCONF = "slides.urls"
ROOT_URAUTH_USER_MODEL = 'userauth.CustomUser'
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "slides/templates",
            os.path.join(BASE_DIR, 'slides/userauth/templates/userauth/'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'slides.blog.context_processors.blog_page',
                'django.template.context_processors.i18n',
            ],
        },
    },
]


WSGI_APPLICATION = "slides.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
#         "ENGINE": "django.db.backends.mysql",
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": "",
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

# Интернационализация
USE_I18N = True

# Локализация
USE_L10N = True

# Использовать часовые пояса
USE_TZ = True

LANGUAGES = [
    ("ru", "Русский"),
    ("en", "English"),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
    os.path.join(BASE_DIR, 'slides/userauth/static/userauth/'),
]

STATIC_ROOT = os.path.join(PROJECT_DIR, "collect_static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")
MEDIA_URL = "/media/"

# Override in local settings or replace with your own key. Please don't use our demo key in production!
#GOOGLE_MAP_API_KEY = "AIzaSyD31CT9P9KxvNUJOwDq2kcFEIG8ADgaFgw"

# Use Elasticsearch as the search backend for extra performance and better search results
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
        "INDEX": "slides",
    },
}

# Wagtail settings
WAGTAIL_SITE_NAME = os.getenv("WAGTAIL_SITE_NAME")


# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'https://Slides.com'


# Slug setting (заголовок в продвижении на русском, англ slug)
# для перевода
# WAGTAIL_ALLOW_UNICODE_SLUGS = False

WAGTAILIMAGES_INDEX_PAGE_SIZE = 32

# https://github.com/adamchainz/django-cors-headers
# TODO: изменить в продакшене
# CORS_ALLOWED_ORIGINS = [
#    "https://example.com",
#    "https://sub.example.com",
#    "http://localhost:8080",
#    "http://127.0.0.1:9000",
# ]
# раньше назывался CORS_ORIGIN_REGEX_WHITELIST
# CORS_ALLOWED_ORIGIN_REGEXES = [
#    r"^https://\w+\.example\.com$",
# ]
CORS_ALLOW_ALL_ORIGINS = True

# Для публикации видео
# WAGTAILEMBEDS_RESPONSIVE_HTML = False

# WAGTAILEMBEDS_FINDERS = [
#    {
#        'class': 'wagtail.embeds.finders.oembed'
#    }
# ]

SITE_ID = 1

COMMENTS_APP = "slides.custom_comments"
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
#CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
#CRISPY_TEMPLATE_PACK = "tailwind"


# custom user model
AUTH_USER_MODEL = 'userauth.CustomUser'

WAGTAIL_USER_CREATION_FORM = 'slides.userauth.forms.WagtailUserCreationForm'
WAGTAIL_USER_EDIT_FORM = 'slides.userauth.forms.WagtailUserEditForm'
WAGTAIL_USER_CUSTOM_FIELDS = ['display_name', 'date_of_birth', 'address1', 'address2', 'zip_code', 'city', 'country', 'mobile_phone', 'additional_information', 'photo',]

# allauth settings
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_FORM_CLASS = 'slides.userauth.forms.SignupForm'
SOCIALACCOUNT_AUTO_SIGNUP = False

# для перевода
#LOGIN_URL = reverse_lazy('account_login')
#LOGIN_REDIRECT_URL = reverse_lazy('account_profile')


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    },
    'linkedin': {
        'SCOPE': [
            'r_basicprofile',
            'r_emailaddress'
        ],
        'PROFILE_FIELDS': [
            'id',
            'first-name',
            'last-name',
            'email-address',
            'picture-url',
            'public-profile-url',
        ],
    },
}
