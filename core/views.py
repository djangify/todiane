from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from blog.models import Post, Category
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from .forms import SupportForm


def home(request):
    """Homepage view."""
    return render(request, "core/home.html")


# -----------------------------------
# POLICY PAGES (breadcrumbs added)
# -----------------------------------
def policies_index_view(request):
    """View function for the policies index page."""
    breadcrumbs = [
        {"title": "Policies", "url": ""},
    ]
    return render(
        request, "core/policy/policies_index.html", {"breadcrumbs": breadcrumbs}
    )


def privacy_view(request):
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "Privacy Policy", "url": ""},
    ]
    return render(request, "core/policy/privacy.html", {"breadcrumbs": breadcrumbs})


def cookie_view(request):
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "Cookie Policy", "url": ""},
    ]
    return render(request, "core/policy/cookies.html", {"breadcrumbs": breadcrumbs})


def affiliate_view(request):
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "Affiliate Policy", "url": ""},
    ]
    return render(request, "core/policy/affiliate.html", {"breadcrumbs": breadcrumbs})


def ai_writing_view(request):
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "AI Writing Policy", "url": ""},
    ]
    return render(
        request, "core/policy/ai-writing-policy.html", {"breadcrumbs": breadcrumbs}
    )


def terms_view(request):
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "Terms & Conditions", "url": ""},
    ]
    return render(request, "core/policy/terms.html", {"breadcrumbs": breadcrumbs})


def handler500(request):
    return render(request, "error/500.html", status=500)


def handler403(request, exception):
    return render(request, "error/403.html", status=403)


def handler404(request, exception):
    # Define which category to show (by slug)
    category_slug = "reflections"  # Change this to your desired category slug

    try:
        # Try to get the category
        category = get_object_or_404(Category, slug=category_slug)

        # Get posts from the category
        category_posts = Post.objects.filter(
            category=category, status="published", publish_date__lte=timezone.now()
        ).order_by("-publish_date")[:4]

    except Http404:
        # Fallback to recent posts if category doesn't exist
        category_posts = Post.objects.filter(
            status="published", publish_date__lte=timezone.now()
        ).order_by("-publish_date")[:6]
        category = None

    context = {"category_posts": category_posts, "selected_category": category}

    return render(request, "error/404.html", context, status=404)


def support(request):
    form = SupportForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Thank you! Your message has been sent.")
        return redirect("core:support")
    return render(request, "core/support.html", {"form": form})


@require_GET
def robots_txt(request):
    """Robots.txt for search + AI visibility."""
    site_url = request.build_absolute_uri("/").rstrip("/")
    sitemap_url = f"{site_url}/sitemap.xml"

    lines = [
        "# robots.txt for todiane.com",
        "# Enables modern search and AI engines to crawl public sections.",
        "",
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Disallow: /media/private/",
        "Disallow: /checkout/",
        "",
        "# AI & Answer Engine Bots",
        "User-agent: GPTBot",
        "User-agent: ChatGPT-User",
        "User-agent: Google-Extended",
        "User-agent: ClaudeBot",
        "User-agent: PerplexityBot",
        "User-agent: anthropic-ai",
        "User-agent: Bingbot",
        "Allow: /",
        "",
        f"Sitemap: {sitemap_url}",
        "",
        "# --- Brand Context ---",
        "# Todiane.com - portfolio projects by Django developer and creator of mini-ecommerce site builder - Diane Corriette.",
        "# It demonstrates best practices in ecommerce,offline-first,AI-search-ready design and ethical tech visibility.",
    ]

    return HttpResponse("\n".join(lines), content_type="text/plain")


# ------------------------------
# STUDIO: MAIN HOMEPAGE
# ------------------------------
def studio_home(request):
    breadcrumbs = [
        {"title": "Studio", "url": ""},
    ]
    return render(request, "core/studio/index.html", {"breadcrumbs": breadcrumbs})


# ------------------------------
# STUDIO: OFFLINE-FIRST APPS
# (all download links removed)
# ------------------------------
def studio_offline_apps(request):
    breadcrumbs = [
        {"title": "Studio", "url": reverse("core:studio_home")},
        {"title": "Offline Apps", "url": ""},
    ]

    context = {"breadcrumbs": breadcrumbs}

    return render(request, "core/studio/offline_apps.html", context)


# ------------------------------
# STUDIO: WEB APPLICATIONS
# ------------------------------
def studio_web_apps(request):
    breadcrumbs = [
        {"title": "Studio", "url": reverse("core:studio_home")},
        {"title": "Web Apps", "url": ""},
    ]
    return render(request, "core/studio/web_apps.html", {"breadcrumbs": breadcrumbs})


# ------------------------------
# STUDIO: PDF PRODUCTS
# ------------------------------
def studio_pdfs(request):
    breadcrumbs = [
        {"title": "Studio", "url": reverse("core:studio_home")},
        {"title": "PDFs", "url": ""},
    ]
    return render(request, "core/studio/pdfs.html", {"breadcrumbs": breadcrumbs})


# ------------------------------
# STUDIO: CREATIVE CODING
# ------------------------------
def studio_creative(request):
    breadcrumbs = [
        {"title": "Studio", "url": reverse("core:studio_home")},
        {"title": "Creative Coding", "url": ""},
    ]
    return render(request, "core/studio/creative.html", {"breadcrumbs": breadcrumbs})


# ------------------------------
# STUDIO: PROJECT CASE STUDIES
# ------------------------------
def studio_projects(request):
    breadcrumbs = [
        {"title": "Studio", "url": reverse("core:studio_home")},
        {"title": "Projects", "url": ""},
    ]
    return render(request, "core/studio/projects.html", {"breadcrumbs": breadcrumbs})


# ------------------------------
# STUDIO: ABOUT THE STUDIO
# ------------------------------
def studio_about(request):
    breadcrumbs = [
        {"title": "Studio", "url": reverse("core:studio_home")},
        {"title": "About", "url": ""},
    ]
    return render(request, "core/studio/about.html", {"breadcrumbs": breadcrumbs})
