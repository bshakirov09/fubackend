from rest_framework import serializers

from fitness.account.constants import DeviceType
from fitness.account.utils import facebook, google
from fitness.account.utils.apple import Apple


class FacebookSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    device = serializers.CharField(required=False)

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)
        if not user_data:
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again."
            )
        if user_data and not user_data.get("email"):
            raise serializers.ValidationError(
                "We could not find your email from your Facebook account"
            )
        return user_data


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    device = serializers.CharField(required=False)

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        if not user_data:
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again."
            )
        return user_data


class AppleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField(required=True)
    device_type = serializers.ChoiceField(
        choices=DeviceType.choices, required=True
    )

    def validate(self, attrs):
        auth_token = attrs.pop("auth_token")
        device_type = attrs.pop("device_type")
        apple = Apple(device_type)
        user_data = apple.do_auth(auth_token)
        if not user_data:
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again."
            )
        attrs.update(user_data)
        return attrs
