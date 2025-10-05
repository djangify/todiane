# todiane/urls.py (project-level)
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("blog/", include("blog.urls", namespace="blog")),
    path("core/", include("core.urls", namespace="core")),
    path("prompts/", include("prompt_generator.urls")),
    path("prompt_templates/", include("prompt_templates.urls")),
]
