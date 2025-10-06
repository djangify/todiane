from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import PromptTemplate
from .forms import PromptFillForm
from .utils import generate_prompt


def template_list_view(request):
    templates = PromptTemplate.objects.all().order_by("-created_at")
    return render(
        request, "prompt_templates/prompt_templates_list.html", {"templates": templates}
    )


def prompt_fill_view(request, slug):
    template = get_object_or_404(PromptTemplate, slug=slug)
    base_text = template.template_text

    # Define all possible placeholders
    placeholders = [
        "business_name",
        "business_type",
        "business_location",
        "target_audience",
        "product_or_service",
        "service_name",
        "topic",
        "industry_topic",
        "additional_info",
    ]

    # Only show fields that appear in the current template
    used_fields = [field for field in placeholders if f"[{field}]" in base_text]

    form = PromptFillForm(request.POST or None)
    for field in list(form.fields.keys()):
        if field not in used_fields:
            form.fields.pop(field)

    generated = None

    if request.method == "POST" and form.is_valid():
        generated = generate_prompt(base_text, request.user, form.cleaned_data)
        if "download" in request.POST:
            response = HttpResponse(generated, content_type="text/plain")
            filename = f"{template.slug}.txt"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

    return render(
        request,
        "prompt_templates/prompt_fill.html",
        {
            "template": template,
            "form": form,
            "generated": generated,
            "filled_text": base_text,
        },
    )
