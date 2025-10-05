# apps/prompts/views.py
from django.shortcuts import render, get_object_or_404
from .models import Prompt


# --- List all prompts or filter by category ---
def prompt_list(request):
    category = request.GET.get("category")
    prompts = (
        Prompt.objects.filter(category=category) if category else Prompt.objects.all()
    )
    return render(
        request,
        "prompts/prompt_list.html",
        {"prompts": prompts, "selected_category": category},
    )


def prompt_detail(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk)
    return render(request, "prompts/prompt_detail.html", {"prompt": prompt})
