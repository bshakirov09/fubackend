import django_filters

from fitness.workout.models import WorkoutType


class WorkoutTypeFilter(django_filters.FilterSet):
    class Meta:
        model = WorkoutType
        fields = ("workout",)
