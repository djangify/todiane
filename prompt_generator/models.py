import uuid
from django.db import models


class GeneratedPrompt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(
        "GeneratorTemplate",
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
