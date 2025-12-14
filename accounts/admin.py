from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for custom email-only User model
    """

    ordering = ("email",)
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_verified",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = (
        "is_verified",
        "is_staff",
        "is_active",
        "is_superuser",
    )

    search_fields = ("email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_verified",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    readonly_fields = ("last_login", "date_joined")

    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def get_fieldsets(self, request, obj=None):
        """
        Simplify admin form for non-superusers
        """
        if not request.user.is_superuser:
            return (
                (None, {"fields": ("email",)}),
                (_("Personal info"), {"fields": ("first_name", "last_name")}),
                (_("Status"), {"fields": ("is_verified", "is_active")}),
            )
        return super().get_fieldsets(request, obj)
