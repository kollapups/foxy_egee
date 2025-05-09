from pathlib import Path
import os
from decouple import config  # Импортируем для чтения из .env

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Читаем SECRET_KEY из .env
SECRET_KEY = config("SECRET_KEY")

# Для локальной разработки оставим DEBUG=True, для Timeweb нужно будет установить False
DEBUG = True

# Разрешенные хосты
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "oauth2_provider",  # Это django-oauth-toolkit
    "corsheaders",
    "users",
    "tasks",
    'cookie_consent',
    'django.contrib.sitemaps',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "tasks.middleware.VisitCounterMiddleware",
]

ROOT_URLCONF = "new_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates", BASE_DIR / "tasks" / "templates"],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # "tasks.context_processors.page_visit",
   
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

# Настройки для django-cookie-consent
COOKIE_CONSENT_NAME = "cookie_consent"
COOKIE_CONSENT_EXPIRY = 31536000  # 1 год в секундах

# Категории cookie
COOKIE_CONSENT_CLASSES = {
    "analytics": {
        "title": "Аналитика",
        "description": "Используется для сбора статистики Яндекс.Метрики.",
    },
}

WSGI_APPLICATION = "new_project.wsgi.application"

# Настройки базы данных из .env
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
        "OPTIONS": {"charset": "utf8mb4", 'init_command': "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED; SET NAMES utf8mb4;"},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

AUTH_USER_MODEL = "users.CustomUser"

# Настройки статических файлов
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "tasks/static")]

# Настройки медиафайлов
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Настройки OAuth2 из .env
OAUTH2_PROVIDER = {
    "SCOPES": {"read": "Read scope", "write": "Write scope"},
}

CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
REDIRECT_URI = config("REDIRECT_URI")
AUTHORIZATION_BASE_URL = config("AUTHORIZATION_BASE_URL")
TOKEN_URL = config("TOKEN_URL")

# Настройки CORS
CORS_ORIGIN_ALLOW_ALL = False  # Отключаем для продакшена
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://foxyege.ru",
    "https://foxyege.ru",
]

# Настройки для продакшена
SECURE_SSL_REDIRECT = False  # Установите True после настройки HTTPS на Timeweb
SESSION_COOKIE_SECURE = False  # Установите True после настройки HTTPS
CSRF_COOKIE_SECURE = False  # Установите True после настройки HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
