from decimal import Decimal

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from fitness.core.models import BaseModel
from fitness.document.models import ImageModel, VideoModel
from fitness.workout.managers import (
    GymManager,
    GymTrackManager,
    QuadManager,
    QuadTrackManager,
)


class Workout(BaseModel):
    title = models.CharField(max_length=255)
    order_number = models.PositiveSmallIntegerField(null=True)


class WorkoutType(BaseModel):
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="workout_types"
    )
    title = models.CharField(max_length=255)
    short_description = models.TextField(null=True)
    description = models.TextField()
    day_duration = models.PositiveSmallIntegerField()
    week_duration = models.PositiveSmallIntegerField(
        default=settings.WEEK_DURATION
    )
    min_duration = models.CharField(max_length=20, null=True)
    equipment = ArrayField(
        models.CharField(max_length=256), blank=True, default=list
    )
    image = models.ForeignKey(ImageModel, on_delete=models.SET_NULL, null=True)


class Gym(BaseModel):
    workout_type = models.ForeignKey(
        WorkoutType, on_delete=models.CASCADE, related_name="gyms"
    )
    title = models.CharField(max_length=256, null=True)
    description = models.TextField(null=True)
    week = models.PositiveSmallIntegerField()
    day = models.PositiveSmallIntegerField()
    min_duration = models.CharField(max_length=20, null=True)
    image = models.ForeignKey(ImageModel, on_delete=models.SET_NULL, null=True)

    objects = GymManager()


class Quad(BaseModel):
    gym = models.ForeignKey(
        Gym, on_delete=models.CASCADE, related_name="quads"
    )
    title = models.CharField(max_length=255)
    count = models.CharField(max_length=255)
    video = models.ForeignKey(VideoModel, on_delete=models.SET_NULL, null=True)
    description = models.TextField()

    objects = QuadManager()


class GymTrack(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gym_tracks",
    )
    gym = models.ForeignKey(
        Gym, on_delete=models.CASCADE, related_name="gym_tracks"
    )
    is_completed = models.BooleanField(default=False)
    objects = GymTrackManager()

    class Meta:
        unique_together = ("user", "gym")


class QuadTrack(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quad_tracks",
    )
    quad = models.ForeignKey(
        Quad, on_delete=models.CASCADE, related_name="quad_tracks"
    )
    data = models.DecimalField(
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        default=Decimal("0.00"),
    )

    objects = QuadTrackManager()

    class Meta:
        unique_together = ("user", "quad")
