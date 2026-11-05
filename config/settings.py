"""
Django settings. Driven by environment variables
"""

from pathlib import Path

import django_stubs_ext

from config.env import env

django_stubs_ext.monkeypatch()

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------- CORE

SECRET_KEY = env.SECRET_KEY
DEBUG = env.DEBUG
ALLOWED_HOSTS = env.ALLOWED_HOSTS
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------- APPS

LOCAL_APPS = [
    "apps.accounts",
    "apps.cms",
    "apps.core",
]

THIRD_PARTY_APPS = [
    "django_ckeditor_5",
    "django_vite",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
]

INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS + DJANGO_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS += ["django_browser_reload"]
    MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# ---------------------------------------- DATABASE

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.DB_NAME,
        "USER": env.DB_USER,
        "PASSWORD": env.DB_PASSWORD,
        "HOST": env.DB_HOST,
        "PORT": env.DB_PORT,
    }
}

# ---------------------------------------- AUTH

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

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = ["apps.accounts.backends.VerifiedUserBackend"]

LOGIN_URL = "auth:login"
LOGIN_REDIRECT_URL = "/app/"
LOGOUT_REDIRECT_URL = LOGIN_URL


# ---------------------------------------- I18N

LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ("en", "English"),
]
TIME_ZONE = env.TIMEZONE
USE_I18N = True
USE_TZ = True

# ---------------------------------------- STATIC

STATIC_URL = "static/"
STATICFILES_DIRS: list[Path] = []
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------- FRONTEND

FRONTEND_DIR = BASE_DIR / "frontend"
if (FRONTEND_DIR / "dist").exists():
    STATICFILES_DIRS += [FRONTEND_DIR / "dist"]

DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
        "dev_server_port": 5173,
        "manifest_path": FRONTEND_DIR / "dist" / "manifest.json",
    }
}

# ---------------------------------------- CKEDITOR

CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
CKEDITOR_5_UPLOAD_FILE_TYPES = ["jpg", "jpeg", "png", "gif", "webp"]
CKEDITOR_5_MAX_FILE_SIZE = 5  # MB

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": {
            "items": [
                "heading",
                "|",
                "bold",
                "italic",
                "link",
                "|",
                "bulletedList",
                "numberedList",
                "blockQuote",
                "|",
                "imageUpload",
                "insertTable",
            ],
        },
        "image": {"toolbar": ["imageTextAlternative"]},
        "table": {"contentToolbar": ["tableColumn", "tableRow", "mergeTableCells"]},
    },
}
