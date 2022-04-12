from rest_framework import serializers

from fitness.workout.models import (
    Gym,
    GymTrack,
    Quad,
    QuadTrack,
    Workout,
    WorkoutType,
)


class WorkoutTypeShortSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="image.file")

    class Meta:
        model = WorkoutType
        fields = (
            "id",
            "title",
            "short_description",
            "day_duration",
            "image",
        )


class WorkoutSerializer(serializers.ModelSerializer):
    workout_types = WorkoutTypeShortSerializer(many=True)

    class Meta:
        model = Workout
        fields = ("id", "title", "workout_types")


class WorkoutTypeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="image.file")

    class Meta:
        model = WorkoutType
        fields = (
            "id",
            "title",
            "short_description",
            "description",
            "day_duration",
            "week_duration",
            "min_duration",
            "equipment",
            "image",
        )


class QuadSerializer(serializers.ModelSerializer):
    is_completed = serializers.BooleanField()
    user_data = serializers.CharField()

    class Meta:
        model = Quad
        fields = ("id", "title", "count", "is_completed", "user_data")


class QuadDetailSerializer(serializers.ModelSerializer):
    video = serializers.ImageField(source="video.file")

    class Meta:
        model = Quad
        fields = ("id", "description", "video")


class QuadListSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = Quad
        fields = ("id", "title", "count", "user_data")

    def get_user_data(self, instance):
        user = self.context["request"].user
        track = QuadTrack.objects.filter(user=user, quad=instance).last()
        if track:
            return track.data
        return None


class GymSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Gym
        fields = (
            "id",
            "week",
            "day",
            "min_duration",
            "description",
            "is_completed",
            "quads",
        )

    def to_representation(self, instance):
        self.fields["quads"] = QuadListSerializer(
            many=True, context=self.context
        )
        return super(GymSerializer, self).to_representation(instance)

    def get_is_completed(self, instance):
        user = self.context["request"].user
        track = GymTrack.objects.filter(user=user, gym=instance).last()
        if track:
            return track.is_completed
        return False


class GymDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="image.file")
    is_completed = serializers.SerializerMethodField()
    quads_count = serializers.SerializerMethodField()

    class Meta:
        model = Gym
        fields = ("id", "day", "title", "is_completed", "quads_count", "image")

    def get_is_completed(self, instance):
        user = self.context["request"].user
        track = GymTrack.objects.filter(user=user, gym=instance).last()
        if track:
            return track.is_completed
        return False

    def get_quads_count(self, instance):
        return instance.quads.count()


class QuadTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuadTrack
        fields = ("id", "user", "quad", "data")
        read_only_fields = ("user",)


class GymTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymTrack
        fields = ("id", "user", "gym", "is_completed")
        read_only_fields = ("user", "is_completed")
