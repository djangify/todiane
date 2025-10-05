from django.urls import path
from . import views

app_name = "prompts"

urlpatterns = [
    path("", views.prompt_list, name="prompt_list"),
    path("<int:pk>/", views.prompt_detail, name="prompt_detail"),
]
