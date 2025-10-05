from django.shortcuts import get_object_or_404, render
from prompts.models import Prompt


def generator_list(request):
    prompts = Prompt.objects.all().order_by("-created_at")
    return render(request, "prompt_generator/generator_list.html", {"prompts": prompts})


def generator_detail(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk)
    return render(request, "prompt_generator/generator_detail.html", {"prompt": prompt})
