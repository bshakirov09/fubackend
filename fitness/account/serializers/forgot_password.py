from cfgv import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from fitness.account.constants import AuthType


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    verification_key = serializers.UUIDField()

    def validate(self, attrs):
        password = attrs["password"]
        validate_password(password)
        confirm_password = attrs["confirm_password"]
        if password != confirm_password:
            raise serializers.ValidationError("passwords do not match")
        return attrs


class ForgotPasswordVerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()

    def validate_code(self, code):
        if code not in range(1000, 10000):
            raise ValidationError("Invalid Code")
        return code


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs["email"]
        if (
            not get_user_model()
            .objects.filter(email=email, auth_type=AuthType.EMAIL)
            .exists()
        ):
            raise serializers.ValidationError(
                "Email not registered or registered with social providers"
            )
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    current_password = serializers.CharField()

    def validate(self, attrs):
        password = attrs["password"]
        confirm_password = attrs["confirm_password"]
        current_password = attrs["current_password"]
        user = self.context["request"].user
        if not user.check_password(current_password):
            raise serializers.ValidationError("Password is wrong")
        if password == current_password:
            raise serializers.ValidationError(
                "Password is similar with old one, "
                "please choose another password"
            )
        validate_password(password)
        if password != confirm_password:
            raise serializers.ValidationError("passwords did not match")
        return attrs
