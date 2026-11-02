
from pathlib import Path
import os
from dotenv import load_dotenv


# =========================================================
# RUTAS DEL PROYECTO
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# VARIABLES DE ENTORNO
# =========================================================

load_dotenv(BASE_DIR / ".env")


# =========================================================
# SEGURIDAD GENERAL
# =========================================================

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if host.strip()
]


# =========================================================
# EVA 3 - SEGURIDAD HTTPS EN AWS
# =========================================================

# En AWS, Nginx recibe las conexiones HTTPS
# y las comunica a Django mediante Gunicorn.

if DEBUG:
    SECURE_PROXY_SSL_HEADER = None
else:
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https"
    )


# Cookies seguras en produccion

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG


# Nginx realiza la redireccion HTTP a HTTPS

SECURE_SSL_REDIRECT = False


# =========================================================
# APLICACIONES INSTALADAS
# =========================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Aplicaciones originales de SIGED
    "delegacionesApp",
    "funcionariosApp",

    # EVA 3 - Gestion de usuarios y perfiles
    "usuariosApp",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# CONFIGURACION DE URLS
# =========================================================

ROOT_URLCONF = "config.urls"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND":
            "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

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


# =========================================================
# WSGI
# =========================================================

WSGI_APPLICATION = "config.wsgi.application"


# =========================================================
# BASE DE DATOS MYSQL
# =========================================================

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


# =========================================================
# VALIDACION DE CONTRASENAS
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =========================================================
# IDIOMA Y ZONA HORARIA
# =========================================================

LANGUAGE_CODE = "es-cl"

TIME_ZONE = "America/Santiago"

USE_I18N = True

USE_TZ = True


# =========================================================
# ARCHIVOS ESTATICOS
# =========================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# =========================================================
# EVA 3 - AUTENTICACION
# =========================================================

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "panel_principal"

LOGOUT_REDIRECT_URL = "login"


# =========================================================
# EVA 3 - RECUPERACION DE CONTRASENAS
# =========================================================

# Tiempo de vigencia del enlace de recuperacion:
# 3600 segundos = 60 minutos.

PASSWORD_RESET_TIMEOUT = int(
    os.getenv("PASSWORD_RESET_TIMEOUT", "3600")
)


# =========================================================
# EVA 3 - CORREO ELECTRONICO SMTP
# =========================================================

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = os.getenv(
    "EMAIL_HOST",
    "smtp.gmail.com"
)

EMAIL_PORT = int(
    os.getenv("EMAIL_PORT", "587")
)

EMAIL_USE_TLS = (
    os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
)

EMAIL_USE_SSL = (
    os.getenv("EMAIL_USE_SSL", "False").lower() == "true"
)


# Credenciales privadas obtenidas desde .env

EMAIL_HOST_USER = os.getenv(
    "EMAIL_HOST_USER",
    ""
)

EMAIL_HOST_PASSWORD = os.getenv(
    "EMAIL_HOST_PASSWORD",
    ""
)

DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    EMAIL_HOST_USER or "webmaster@localhost"
)

EMAIL_TIMEOUT = int(
    os.getenv("EMAIL_TIMEOUT", "15")
)


# =========================================================
# CLAVE PRIMARIA POR DEFECTO
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
