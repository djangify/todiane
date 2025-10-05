from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    # cluster pages
    path(
        "pdf-creation",
        TemplateView.as_view(template_name="core/pdf-creation.html"),
        name="pdf_creation",
    ),
    # Project pages
    path(
        "portfolio",
        TemplateView.as_view(template_name="core/projects/portfolio.html"),
        name="portfolio",
    ),
    path(
        "tracker",
        TemplateView.as_view(template_name="core/projects/tracker.html"),
        name="tracker",
    ),
    path(
        "stream",
        TemplateView.as_view(template_name="core/projects/stream.html"),
        name="stream",
    ),
    path(
        "posterpalace",
        TemplateView.as_view(template_name="core/projects/posterpalace.html"),
        name="posterpalace",
    ),
    path(
        "digital-marketing-specialist",
        TemplateView.as_view(template_name="core/digital-marketing-specialist.html"),
        name="digital_marketing_specialist",
    ),
    # policies
    path("policy/privacy/", views.privacy_view, name="privacy_policy"),
    path("policy/cookies/", views.cookie_view, name="cookie_policy"),
    path("policy/affiliate/", views.affiliate_view, name="affiliate_policy"),
    path("policy/ai-writing/", views.ai_writing_view, name="ai_writing_policy"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
