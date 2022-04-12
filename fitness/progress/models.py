from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from fitness.core.models import BaseModel
from fitness.document.models import ImageModel
from fitness.progress.constants import Digestion, IntensityRate, Mood


class Weight(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="progress_weights",
        on_delete=models.CASCADE,
    )
    weight = models.DecimalField(
        decimal_places=settings.DECIMAL_PLACES, max_digits=settings.MAX_DIGITS
    )

    def __str__(self):
        return f"{self.weight}"


class Photo(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="progress_photos",
        on_delete=models.CASCADE,
    )
    front = models.ForeignKey(
        ImageModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="progress_front_photos",
    )
    side = models.ForeignKey(
        ImageModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="progress_side_photos",
    )
    back = models.ForeignKey(
        ImageModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="progress_back_photos",
    )


class Journal(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="progress_journals",
        on_delete=models.CASCADE,
    )
    intensity_rate = models.CharField(
        max_length=30, choices=IntensityRate.choices
    )
    mood = models.CharField(max_length=30, choices=Mood.choices)
    digestion = models.CharField(max_length=30, choices=Digestion.choices)
    period = models.BooleanField()
    water_goal_days = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(7), MinValueValidator(0)]
    )
    step_goal_days = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(7), MinValueValidator(0)]
    )
    notes = models.TextField()
