from django.contrib.auth import get_user_model
from rest_framework import serializers

from fitness.document.serializers import ImageModelSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
            "profile_image",
            "gender",
            "height",
            "weight",
            "date_of_birth",
            "auth_type",
            "email",
        )

        extra_kwargs = {
            "full_name": {"read_only": True},
            "first_name": {
                "required": False,
                "allow_null": False,
            },
            "last_name": {
                "required": False,
                "allow_null": False,
            },
            "auth_type": {"read_only": True},
            "email": {"read_only": True},
        }

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        action = kwargs["context"]["view"].action
        if action in ["list", "detail", "get_profile"]:
            self.fields["profile_image"] = ImageModelSerializer()
