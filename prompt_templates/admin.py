from django.contrib import admin
from .models import PromptTemplate


@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    """Admin configuration for Prompt Template entries."""

    # Displayed in the list view
    list_display = ("title", "category", "created_at")

    # Allow quick inline category editing in the list view
    list_editable = ("category",)

    # Search box fields
    search_fields = ("title", "template_text", "tips")

    # Filters in sidebar
    list_filter = ("category", "created_at")

    # Default order (newest first)
    ordering = ("-created_at",)

    # Define how the form is grouped in the admin
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "template_text", "tips")}),
        (
            "Metadata",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    # Make certain fields read-only
    readonly_fields = ("created_at", "slug")
