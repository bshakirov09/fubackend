from django.db import models

from fitness.core.utils.utils import get_or_none


class GymManager(models.Manager):
    def get_list(self, request):
        from fitness.workout.mobile.serializers import GymDetailSerializer
        from fitness.workout.models import WorkoutType

        params = request.query_params

        workout_type = get_or_none(WorkoutType, id=params.get("workout_type"))
        if workout_type is None:
            return {}
        qs = (
            self.filter(workout_type=workout_type)
            .order_by("week")
            .order_by("day")
        )
        result = dict()
        for i in range(1, workout_type.week_duration + 1):
            result[i] = GymDetailSerializer(
                qs.filter(week=i), many=True, context={"request": request}
            ).data
        return result


class QuadManager(models.Manager):
    pass


class QuadTrackManager(models.Manager):
    def create_quad_track(self, data, user):
        return self.update_or_create(
            user=user, quad=data.pop("quad"), defaults=dict(**data)
        )[0]


class GymTrackManager(models.Manager):
    def create_gym_track(self, data, user):
        gym = data["gym"]
        gym_track, _ = self.get_or_create(gym=gym, user=user)
        gym_track.is_completed = True
        gym_track.save()
        return gym_track
