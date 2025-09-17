import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "change-me"
DEBUG_MAGIC = "5ebe2294ecd0e0f08eab7690d2a6ee69"
ADMIN_MAGIC = "secret-admin-url/"

DEBUG = False
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django_extensions",
    "myauth",
    "notes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'noteapp.middleware.SecurityHeadersMiddleware',

]

ROOT_URLCONF = "noteapp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Message templates (for CSS)
from django.contrib.messages import constants as message_constants
 
MESSAGE_TAGS = {
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.ERROR: 'danger'
}

WSGI_APPLICATION = "noteapp.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
  {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
  {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator','OPTIONS':{'min_length':12}},
  {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
  {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Pacific/Auckland"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT=os.path.join(BASE_DIR, "staticroot")
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# cookies
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 1800


# Login URLs
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "note_list"
LOGOUT_REDIRECT_URL = "login"

# Email settings
# Run a console SMTP backend with `python3 -m aiosmtpd -n -l localhost:8025`
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 8025
EMAIL_USE_TLS = False
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""

# Logging setup
LOGFILE = "all.log"
LOGGING_PATH = os.path.join(MEDIA_ROOT, "logs")
os.makedirs(LOGGING_PATH, exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGGING_PATH, LOGFILE),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.utils.autoreload": {
            "handlers": ["file"],
            "level": "WARN",
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
        "noteapp": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "notes": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {name} {asctime} - {module} {process:d} : {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
}