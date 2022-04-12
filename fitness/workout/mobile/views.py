from rest_framework import mixins
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from fitness.workout.mobile.serializers import (
    GymSerializer,
    GymTrackSerializer,
    QuadDetailSerializer,
    QuadTrackSerializer,
    WorkoutSerializer,
    WorkoutTypeSerializer,
)
from fitness.workout.models import (
    Gym,
    GymTrack,
    Quad,
    QuadTrack,
    Workout,
    WorkoutType,
)


class WorkoutListView(ListAPIView):
    queryset = Workout.objects.all().order_by("order_number")
    serializer_class = WorkoutSerializer


class WorkoutTypeDetailView(RetrieveAPIView):
    queryset = WorkoutType.objects.all()
    serializer_class = WorkoutTypeSerializer
    lookup_field = "id"


class QuadTrackViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = QuadTrack.objects.all()
    serializer_class = QuadTrackSerializer

    def perform_create(self, serializer):
        serializer.instance = QuadTrack.objects.create_quad_track(
            serializer.validated_data, self.request.user
        )


class GymTrackViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = GymTrack.objects.all()
    serializer_class = GymTrackSerializer

    def perform_create(self, serializer):
        serializer.instance = GymTrack.objects.create_gym_track(
            serializer.validated_data, self.request.user
        )


class RoadMapView(APIView):
    def get(self, request, *args, **kwargs):
        gyms = Gym.objects.get_list(request)
        return Response(gyms)


class GymRetrieveView(RetrieveAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    lookup_field = "id"


class QuadRetrieveView(RetrieveAPIView):
    queryset = Quad.objects.all()
    serializer_class = QuadDetailSerializer
    lookup_field = "id"
