# todiane/urls.py (project-level)
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("", include("blog.urls", namespace="blog")),
    path("prompts/", include("prompt_generator.urls")),
    path("prompt_templates/", include("prompt_templates.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
