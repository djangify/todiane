# You only need this if you want to manage it in admin.py so uncomment once you do

# from django.contrib import admin
# from .models import Prompt


# @admin.register(Prompt)
# class PromptAdmin(admin.ModelAdmin):
#     list_display = ("title", "category", "created_at")
#     list_filter = ("category", "created_at")
#     search_fields = ("title", "content", "tags")
#     ordering = ("-created_at",)
#     fields = ("title", "content", "category", "tags")
#     readonly_fields = ("created_at",)
