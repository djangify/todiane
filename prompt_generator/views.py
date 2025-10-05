from django.shortcuts import render, get_object_or_404
from .models import GeneratorTemplate, GeneratedPrompt, GeneratorCategory
from django.http import JsonResponse


def generator_list(request):
    """Display all active generator templates."""
    category_slug = request.GET.get("category")

    if category_slug:
        templates = GeneratorTemplate.objects.filter(
            is_active=True, category__slug=category_slug
        ).select_related("category")
    else:
        templates = GeneratorTemplate.objects.filter(is_active=True).select_related(
            "category"
        )

    categories = GeneratorCategory.objects.filter(is_active=True).order_by("order")

    context = {
        "templates": templates,
        "categories": categories,
        "selected_category": category_slug,
    }
    return render(request, "prompt_generator/generator_list.html", context)


def generator_detail(request, pk):
    """Show details of a specific generator template."""
    template = get_object_or_404(GeneratorTemplate, pk=pk)
    parameters = template.parameters.all().order_by("order")

    context = {
        "template": template,
        "parameters": parameters,
    }
    return render(request, "prompt_generator/generator_detail.html", context)


def generate_prompt_view(request, pk):
    """Generate prompt output via POST."""
    template = get_object_or_404(GeneratorTemplate, pk=pk)

    if request.method == "POST":
        params = {key: value for key, value in request.POST.items()}
        text = template.template_text
        for key, value in params.items():
            text = text.replace(f"{{{key}}}", value)

        generated = GeneratedPrompt.objects.create(
            template=template,
            name=f"Generated from {template.name}",
            prompt_text=text,
            parameters_used=params,
        )

        return JsonResponse({"result": text})

    return JsonResponse({"error": "Invalid request method."}, status=400)
