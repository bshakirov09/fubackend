from django.db import models

from fitness.core.models import BaseModel
from fitness.document.models import ImageModel


class Blog(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    podcast = models.URLField(null=True, blank=True)
    image = models.ForeignKey(
        ImageModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class BlogImages(BaseModel):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="blog_images",
        related_query_name="blog_images",
    )
    image = models.ForeignKey(
        ImageModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
