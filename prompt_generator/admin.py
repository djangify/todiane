from django.contrib import admin
from .models import GeneratedPrompt


@admin.register(GeneratedPrompt)
class GeneratedPromptAdmin(admin.ModelAdmin):
    list_display = ("name", "template", "token_count", "created_at")
    list_filter = ("template", "created_at")
    search_fields = ("name", "prompt_text")
    readonly_fields = ("token_count", "created_at")
