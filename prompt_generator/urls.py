from django.urls import path
from . import views

app_name = "prompt_generator"

urlpatterns = [
    path("", views.generator_list, name="generator_list"),
    path("<uuid:pk>/", views.generator_detail, name="generator_detail"),
]
