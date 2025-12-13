# core/models.py
from django.db import models


class SupportRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} from {self.name}"


class Gallery(models.Model):
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional short description shown under the gallery title.",
    )
    slug = models.SlugField(unique=True)
    published = models.BooleanField(default=True)


class GalleryImage(models.Model):
    gallery = models.ForeignKey(
        Gallery,
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="gallery/")
    title = models.CharField(max_length=200, blank=True)
    caption = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title or f"Image {self.pk}"
