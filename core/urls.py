from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    # cluster pages
    path(
        "ai-search-readiness/",
        TemplateView.as_view(template_name="core/ai-search-readiness.html"),
        name="ai_search",
    ),
    path(
        "independent-software/",
        TemplateView.as_view(template_name="core/independent-software.html"),
        name="independent_software",
    ),
    # STUDIO PAGES
    path("studio/", views.studio_home, name="studio_home"),
    path("studio/offline-apps/", views.studio_offline_apps, name="studio_offline_apps"),
    path("studio/web-apps/", views.studio_web_apps, name="studio_web_apps"),
    path("studio/pdfs/", views.studio_pdfs, name="studio_pdfs"),
    path("studio/creative/", views.studio_creative, name="studio_creative"),
    path("studio/projects/", views.studio_projects, name="studio_projects"),
    path("studio/about/", views.studio_about, name="studio_about"),
    # policies
    path("policy/privacy/", views.privacy_view, name="privacy_policy"),
    path("policy/cookies/", views.cookie_view, name="cookie_policy"),
    path("policy/terms/", views.terms_view, name="terms_policy"),
    path("policy/affiliate/", views.affiliate_view, name="affiliate_policy"),
    path("policy/ai-writing/", views.ai_writing_view, name="ai_writing_policy"),
    path("policy/", views.policies_index_view, name="policies_index"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
