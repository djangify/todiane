from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.urls import reverse
from blog.models import Post, Category
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib import messages
from .forms import SupportForm


def home(request):
    """Homepage view."""
    return render(request, "core/home.html")


def privacy_view(request):
    """Display the Privacy Policy page."""
    return render(request, "core/policy/privacy.html")


def cookie_view(request):
    """Display the Cookie Policy page."""
    return render(request, "core/policy/cookies.html")


def affiliate_view(request):
    """Display the Affiliate Policy page."""
    return render(request, "core/policy/affiliate.html")


def ai_writing_view(request):
    """Display the AI Writing Policy page."""
    return render(request, "core/policy/ai-writing-policy.html")


def handler500(request):
    return render(request, "error/500.html", status=500)


def handler403(request, exception):
    return render(request, "error/403.html", status=403)


def handler404(request, exception):
    # Define which category to show (by slug)
    category_slug = "projects"  # Change this to your desired category slug

    try:
        # Try to get the category
        category = get_object_or_404(Category, slug=category_slug)

        # Get posts from the category
        category_posts = Post.objects.filter(
            category=category, status="published", publish_date__lte=timezone.now()
        ).order_by("-publish_date")[:8]

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
        form.save()  # saves to DB + emails + auto-ack
        messages.success(request, "Thank you! Your message has been sent.")
        return redirect("core:support")
    return render(request, "core/support.html", {"form": form})


@require_GET
def robots_txt(request):
    site_url = request.build_absolute_uri("/").rstrip("/")
    sitemap_url = f"{site_url}/sitemap.xml"

    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Disallow: /static/",
        "",
        f"Sitemap: {sitemap_url}",
    ]

    return HttpResponse("\n".join(lines), content_type="text/plain")
