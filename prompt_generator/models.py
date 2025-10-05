import uuid
from django.db import models


class GeneratorCategory(models.Model):
    """Categories to group templates (e.g. Marketing, SEO, Blog)"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Generator Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class GeneratorTemplate(models.Model):
    """Prompt template with parameters and text placeholders."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        GeneratorCategory,
        on_delete=models.CASCADE,
        related_name="templates",
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    template_text = models.TextField(
        help_text="Use {parameter_name} for replaceable parameters"
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class GeneratorParameter(models.Model):
    """Dynamic fields that define inputs for a GeneratorTemplate."""

    PARAMETER_TYPES = (
        ("text", "Text Input"),
        ("select", "Select Dropdown"),
        ("radio", "Radio Button"),
        ("checkbox", "Checkbox"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(
        GeneratorTemplate,
        on_delete=models.CASCADE,
        related_name="parameters",
    )
    name = models.CharField(
        max_length=50,
        help_text="Parameter name used in template (e.g. business_name)",
    )
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parameter_type = models.CharField(
        max_length=20, choices=PARAMETER_TYPES, default="text"
    )
    options = models.TextField(
        blank=True,
        null=True,
        help_text="Comma-separated options for select/radio/checkbox",
    )
    default_value = models.CharField(max_length=200, blank=True)
    is_required = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.display_name} ({self.name})"


class GeneratedPrompt(models.Model):
    """Saved output from a generated template."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(
        GeneratorTemplate,
        on_delete=models.SET_NULL,
        null=True,
        related_name="generated_prompts",
    )
    name = models.CharField(max_length=100)
    prompt_text = models.TextField()
    parameters_used = models.JSONField(default=dict)
    token_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
