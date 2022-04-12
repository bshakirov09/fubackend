from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fitness.account.constants import GENDER
from fitness.document.serializers import ImageModelMiniSerializer
from fitness.progress.constants import ActivityLevel, Direction
from fitness.progress.models import Journal, Photo, Weight


class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = ("id", "user", "weight", "created_dttm")

        extra_kwargs = {
            "user": {"read_only": True},
            "created_dttm": {"read_only": True},
        }

    def validate(self, attrs):
        if self.context["view"].action == "create":
            if self.Meta.model.objects.filter(
                created_dttm__date=datetime.now().date()
            ).exists():
                raise ValidationError(
                    "Weight has been already added for today"
                )
        return attrs


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("id", "user", "front", "side", "back", "created_dttm")

        extra_kwargs = {
            "user": {"read_only": True},
            "created_dttm": {"read_only": True},
            "front": {"required": True},
            "side": {"required": True},
            "back": {"required": True},
        }

    def __init__(self, *args, **kwargs):
        super(PhotoSerializer, self).__init__(*args, **kwargs)
        action = kwargs["context"]["view"].action
        if action in ["list", "retrieve", "detail_view"]:
            self.fields["front"] = serializers.ImageField(source="front.file")
            self.fields["side"] = serializers.ImageField(source="side.file")
            self.fields["back"] = serializers.ImageField(source="back.file")
            self.fields.pop("user")
        elif action == "add_photo_check":
            self.fields["front"] = ImageModelMiniSerializer()
            self.fields["side"] = ImageModelMiniSerializer()
            self.fields["back"] = ImageModelMiniSerializer()
            self.fields.pop("user")

    def validate(self, attrs):
        if self.context["view"].action == "create":
            if self.Meta.model.objects.filter(
                created_dttm__date=datetime.now().date()
            ).exists():
                raise ValidationError("Photo has been already added for today")
        return attrs


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = (
            "id",
            "user",
            "intensity_rate",
            "mood",
            "digestion",
            "period",
            "water_goal_days",
            "step_goal_days",
            "notes",
            "created_dttm",
        )

        extra_kwargs = {
            "user": {"read_only": True},
            "created_dttm": {"read_only": True},
        }

    def validate(self, attrs):
        if self.context["view"].action == "create":
            if self.Meta.model.objects.filter(
                created_dttm__date=datetime.now().date()
            ).exists():
                raise ValidationError(
                    "Journal has been already added for today"
                )
        return attrs


class JournalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = (
            "id",
            "intensity_rate",
            "mood",
            "digestion",
            "period",
            "created_dttm",
        )


class PhotoDetailNextSerializer(serializers.Serializer):
    direction = serializers.ChoiceField(choices=Direction.choices)
    current_date = serializers.DateField()


class CalculatorRMRSerializer(serializers.Serializer):
    height = serializers.IntegerField(required=True)
    weight = serializers.DecimalField(
        max_digits=8, decimal_places=2, required=True
    )
    activity_level = serializers.ChoiceField(
        choices=ActivityLevel.choices, required=True
    )
    gender = serializers.ChoiceField(choices=GENDER.choices, required=True)
    age = serializers.IntegerField(required=True)


class DaySerializer(serializers.Serializer):
    day1 = serializers.IntegerField(required=True)
    day2 = serializers.IntegerField(required=True)
    day3 = serializers.IntegerField(required=True)


class CalculateMacrosIntakeSerializer(serializers.Serializer):
    protein = DaySerializer()
    carbohydrates = DaySerializer()
    fats = DaySerializer()
    calories = DaySerializer()
