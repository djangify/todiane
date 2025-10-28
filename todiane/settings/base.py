from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environment setup
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

SITE_URL = env("SITE_URL", default="http://localhost:8000")
SECRET_KEY = env("SECRET_KEY", default="unsafe-secret-key")

DEBUG = False

ALLOWED_HOSTS = ["*"]

SITE_ID = 1

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.redirects",
    "django.contrib.sites",
    "blog",
    "core",
    "prompt_generator",
    "prompts",
    "prompt_templates",
    "portfolio",
    "widget_tweaks",
    "tinymce",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "todiane.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "todiane.wsgi.application"

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TINYMCE_DEFAULT_CONFIG = {
    "height": 700,
    "menubar": False,
    "statusbar": True,
    "branding": False,
    "plugins": "lists paste link autolink code preview fullscreen wordcount image",
    "toolbar": (
        "undo redo | blocks | bold italic | bullist numlist | "
        "link image | removeformat | preview fullscreen | code"
    ),
    "block_formats": "Paragraph=p; Heading 2=h2; Heading 3=h3",
    "forced_root_block": "p",
    "paste_as_text": True,
    "paste_data_images": False,
    # Allow <img> with useful attributes
    "valid_elements": (
        "p,strong/b,em/i,h2,h3,ul,ol,li,a[href|title|target|rel],br,"
        "img[src|alt|width|height|class|style]"
    ),
    "extended_valid_elements": (
        "a[href|title|target|rel],img[src|alt|width|height|class|style]"
    ),
    "valid_children": "+ol[li],+ul[li]",
    "convert_urls": True,
    "relative_urls": False,
    "remove_script_host": False,
    # Make inserted images responsive & centered
    "content_style": (
        "body{font-family:Poppins,system-ui,sans-serif;line-height:1.7;}"
        "h2{font-size:1.5rem;font-weight:700;margin:1rem 0 .5rem;}"
        "h3{font-size:1.25rem;font-weight:600;margin:.75rem 0 .25rem;}"
        "p{margin:.75rem 0;} ul,ol{margin:.5rem 0 1rem;padding-left:1.25rem;}"
        "li{margin:.25rem 0;} strong{font-weight:600;}"
        "img{max-width:100%;height:auto;display:block;margin:1rem auto;}"
    ),
    # Configure image dialog so it only asks for a URL + alt text
    "image_dimensions": False,  # hides width/height boxes
    "image_class_list": [
        {"title": "Responsive (50%)", "value": "img-half"},
        {"title": "Full width", "value": "img-full"},
    ],
}
