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
    form = PromptFillForm(request.POST or None)
    generated = None
    base_text = template.template_text

    if request.method == "POST" and form.is_valid():
        generated = generate_prompt(base_text, None, form.cleaned_data)
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
