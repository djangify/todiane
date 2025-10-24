# todiane/urls.py (project-level)
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from todiane.sitemap import StaticViewSitemap, BlogPostSitemap, PortfolioSitemap


sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogPostSitemap,
    "portfolio": PortfolioSitemap,
}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("prompts/", include("prompts.urls", namespace="prompts")),
    path(
        "prompt_templates/",
        include("prompt_templates.urls", namespace="prompt_templates"),
    ),
    path("portfolio/", include("portfolio.urls", namespace="portfolio")),
    path("", include("core.urls", namespace="core")),
    path(
        "", include("blog.urls", namespace="blog")
    ),  # must stay at the bottom to avoid url conflicts
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "core.views.handler404"
handler500 = "core.views.handler500"
handler403 = "core.views.handler403"
