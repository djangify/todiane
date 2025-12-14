from .base import *  # noqa: F403

DEBUG = False

ALLOWED_HOSTS = [
    "todiane.com",
    "www.todiane.com",
    "www.todiane.dev",
    "todiane.dev",
    "www.dianecorriette.com",
    "dianecorriette.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://todiane.com",
    "https://www.todiane.com",
    "https://dianecorriette.com",
    "https://www.dianecorriette.com",
    "https://todiane.dev",
    "https://www.todiane.dev",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DATABASE_NAME"),  # noqa: F405
        "USER": env("DATABASE_USER"),  # noqa: F405
        "PASSWORD": env("DATABASE_PASSWORD"),  # noqa: F405
        "HOST": env("DATABASE_HOST", default="localhost"),  # noqa: F405
        "PORT": env("DATABASE_PORT", default="5432"),  # noqa: F405
    }
}

# Session Configuration
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_NAME = "sessionid"  # Change back to standard name
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True  # Change back to True for security
SESSION_COOKIE_PATH = "/"

# Security settings
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True


SITE_URL = "https://www.todiane.com"


from logging_config import LOGGING  # noqa: F401, E402


# Admin configuration
ADMINS = [
    (
        env("ADMIN_NAME", default="Admin"),  # noqa: F405
        env("ADMIN_EMAIL", default="noreply@todiane.com"),  # noqa: F405
    ),
]

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@todiane.com")  # noqa: F405
SERVER_EMAIL = env("SERVER_EMAIL", default="noreply@todiane.com")  # noqa: F405

# Additional security headers
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Email settings for production
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mail.privateemail.com")  # noqa: F405
EMAIL_PORT = env("EMAIL_PORT", default=587)  # noqa: F405
EMAIL_HOST_USER = env("EMAIL_HOST_USER")  # noqa: F405
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")  # noqa: F405
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
