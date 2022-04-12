from django.contrib import admin

from fitness.workout.models import (
    Gym,
    GymTrack,
    Quad,
    QuadTrack,
    Workout,
    WorkoutType,
)

admin.site.register(Workout)
admin.site.register(WorkoutType)
admin.site.register(QuadTrack)
admin.site.register(GymTrack)
admin.site.register(Gym)
admin.site.register(Quad)
