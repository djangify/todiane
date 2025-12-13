from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post
from portfolio.models import Portfolio
from datetime import datetime
from core.models import Gallery


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        # Key static / informational pages
        def items(self):
            return [
                "core:home",
                "core:ai_search",
                "core:independent_software",
                # studio
                "core:studio_home",
                "core:studio_offline_apps",
                "core:studio_web_apps",
                "core:studio_pdfs",
                "core:studio_creative",
                "core:studio_projects",
                "core:studio_about",
                # policies
                "core:privacy_policy",
                "core:cookie_policy",
                "core:terms_policy",
                "core:affiliate_policy",
                "core:ai_writing_policy",
                "core:policies_index",
            ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return datetime.now()


class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return obj.get_absolute_url()


class PortfolioSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Portfolio.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class GallerySitemap(Sitemap):
    priority = 0.9
    changefreq = "monthly"

    def items(self):
        return Gallery.objects.filter(published=True)

    def location(self, obj):
        return reverse("core:gallery", kwargs={"slug": obj.slug})
