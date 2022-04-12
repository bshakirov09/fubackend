from rest_framework import serializers

from fitness.core.constants import PageChoices


class VersionControlSerializer(serializers.Serializer):
    page = serializers.ChoiceField(choices=PageChoices.choices)
    detail_id = serializers.IntegerField(required=False)
