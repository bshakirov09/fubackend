from rest_framework import serializers

from fitness.document.serializers import (
    ImageModelMiniSerializer,
    VideoModelSerializer,
)
from fitness.workout.models import Gym, Quad, Workout, WorkoutType


class WorkoutAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ("id", "title", "description", "image")

    def __init__(self, *args, **kwargs):
        super(WorkoutAdminSerializer, self).__init__(*args, **kwargs)
        action = kwargs["context"]["view"].action
        if action in ["list", "retrieve"]:
            self.fields["image"] = ImageModelMiniSerializer()


class WorkoutTypeAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutType
        fields = (
            "id",
            "workout",
            "title",
            "description",
            "day_duration",
            "week_duration",
            "image",
        )

    def __init__(self, *args, **kwargs):
        super(WorkoutTypeAdminSerializer, self).__init__(*args, **kwargs)
        action = kwargs["context"]["view"].action
        if action in ["list", "retrieve"]:
            self.fields["image"] = ImageModelMiniSerializer()
            self.fields["workout"] = WorkoutAdminSerializer(**kwargs)


class GymAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ("id", "workout_type", "week", "day", "image")

    def __init__(self, *args, **kwargs):
        super(GymAdminSerializer, self).__init__(*args, **kwargs)
        action = kwargs["context"]["view"].action
        if action in ["list", "retrieve"]:
            self.fields["image"] = ImageModelMiniSerializer()


class QuadAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quad
        fields = ("id", "gym", "title", "count", "description", "video")

    def __init__(self, *args, **kwargs):
        super(QuadAdminSerializer, self).__init__(*args, **kwargs)
        action = kwargs["context"]["view"].action
        if action in ["list", "retrieve"]:
            self.fields["video"] = VideoModelSerializer()
