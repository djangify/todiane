from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post
from portfolio.models import Portfolio
from datetime import datetime


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        # Key static / informational pages
        return [
            "core:home",
            "core:ai_search",
            "core:local_ai_search",
            "core:privacy_policy",
            "core:cookie_policy",
            "core:affiliate_policy",
            "core:ai_writing_policy",
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
