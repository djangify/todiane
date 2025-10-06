from django.db import models


class Prompt(models.Model):
    CATEGORY_CHOICES = [
        ("ads", "Advertising"),
        ("blog", "Blog & Content"),
        ("customer", "Customer Engagement"),
        ("email", "Email Marketing"),
        ("general", "General"),
        ("local", "Local Business"),
        ("marketing", "Marketing"),
        ("sales", "Sales Pages"),
        ("seo", "SEO"),
        ("social", "Social Media"),
        ("video", "Video Scripts"),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField(help_text="The actual prompt text")
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="marketing"
    )
    tags = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated tags"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
