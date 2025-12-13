# core/admin.py
from django.contrib import admin
from .models import SupportRequest
from .models import Gallery, GalleryImage


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "created_at", "handled")
    list_filter = ("handled", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 0
    readonly_fields = ("admin_thumbnail",)
    fields = (
        "admin_thumbnail",
        "image",
        "caption",
        "order",
        "published",
    )


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "subtitle", "published")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [GalleryImageInline]
    list_filter = ("published",)
    search_fields = ("title",)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "gallery", "order", "published")
    list_filter = ("published", "gallery")
    ordering = ("gallery", "order")
