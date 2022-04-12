from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from fitness.workout.dashboard.serializers import (
    GymAdminSerializer,
    QuadAdminSerializer,
    WorkoutAdminSerializer,
    WorkoutTypeAdminSerializer,
)
from fitness.workout.models import Gym, Quad, Workout, WorkoutType


class WorkoutViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Workout.objects.all()
    serializer_class = WorkoutAdminSerializer


class WorkoutTypeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = WorkoutType.objects.all()
    serializer_class = WorkoutTypeAdminSerializer


class GymViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Gym.objects.all()
    serializer_class = GymAdminSerializer


class QuadViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Quad.objects.all()
    serializer_class = QuadAdminSerializer
