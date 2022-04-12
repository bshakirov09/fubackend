from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from fitness.account.constants import GENDER, AuthType


class LogInSerializer(TokenObtainPairSerializer):
    device = serializers.CharField(required=False)

    def validate(self, attrs):
        validate_email(attrs["email"])
        user = get_user_model().objects.filter(email=attrs["email"]).first()
        if not user:
            raise AuthenticationFailed("User not found with this email")
        if not user.check_password(attrs["password"]):
            raise AuthenticationFailed("Password is wrong")
        if user.auth_type != AuthType.EMAIL:
            raise ValidationError(
                "This email has been registered with social sign in providers"
            )
        device = attrs.get("device")
        super().validate(attrs)
        if device and device not in self.user.devices:
            self.user.devices.append(device)
            self.user.save()
        attrs = {
            "type": "AUTHENTICATED",
            "info": {
                "full_name": self.user.full_name,
                "gender": self.user.gender,
                "tokens": self.user.tokens(),
            },
        }
        return attrs


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.ChoiceField(GENDER.choices, required=False)
    password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if get_user_model().objects.filter(
            email=attrs["email"], is_active=True
        ):
            raise ValidationError("User with this email already exists.")
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords did not match")
        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"] = serializers.EmailField()
        self.fields["code"] = serializers.IntegerField()

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        user = get_object_or_404(get_user_model(), email=attrs["email"])
        cache_code = cache.get(attrs["email"])
        if cache_code != attrs["code"]:
            raise ValidationError("Verification is wrong")
        user.is_active = True
        user.save()
        data = super().validate(attrs)
        data.update(
            type="AUTHENTICATED",
            info={
                "full_name": user.full_name,
                "gender": user.gender,
                "tokens": user.tokens(),
            },
        )
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        data.pop("code")
        data.pop("email")
        return data


class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    device = serializers.CharField(required=False)
