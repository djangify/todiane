from django.contrib import admin

from .models import AccountStatus, EmailVerificationToken, MemberResource


@admin.register(AccountStatus)
class AccountStatusAdmin(admin.ModelAdmin):
    list_display = ("user", "is_verified", "verified_at")
    list_filter = ("is_verified",)
    search_fields = ("user__email", "user__username")


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at")
    search_fields = ("user__email", "user__username")
    readonly_fields = ("token", "created_at")


@admin.register(MemberResource)
class MemberResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
