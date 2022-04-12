import uuid

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from fitness.account.serializers.email_auth import (
    LogInSerializer,
    LogOutSerializer,
    RegisterSerializer,
    VerifyEmailSerializer,
)
from fitness.account.serializers.forgot_password import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ForgotPasswordVerifyEmailSerializer,
    ResetPasswordSerializer,
)
from fitness.account.serializers.social_auth import (
    AppleSocialAuthSerializer,
    FacebookSocialAuthSerializer,
    GoogleSocialAuthSerializer,
)
from fitness.account.serializers.user import UserSerializer
from fitness.account.utils.mail import send_email
from fitness.account.utils.register import register_social_user


class GoogleSocialAuthView(GenericAPIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = GoogleSocialAuthSerializer

    def map_user_data(self, data):
        user_data = dict()
        user_data["email"] = data["email"]
        user_data["first_name"] = data.get("given_name")
        user_data["last_name"] = data.get("family_name")
        user_data["device"] = data["device"]
        return user_data

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data["auth_token"]
        data["device"] = serializer.validated_data.get("device")
        result = register_social_user(**self.map_user_data(data))
        return Response(result, status=status.HTTP_201_CREATED)


class FacebookSocialAuthView(GenericAPIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = FacebookSocialAuthSerializer

    def map_user_data(self, data):
        user_data = dict()
        user_data["email"] = data["email"]
        user_data["first_name"] = data.get("given_name")
        user_data["last_name"] = data.get("family_name")
        user_data["device"] = data["device"]
        return user_data

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data["auth_token"]
        data["device"] = serializer.validated_data.get("device")
        result = register_social_user(**self.map_user_data(data))
        return Response(result, status=status.HTTP_201_CREATED)


class AppleSocialAuthView(GenericAPIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = AppleSocialAuthSerializer

    def map_user_data(self, data):
        user_data = dict()
        user_data["email"] = data["email"]
        user_data["first_name"] = data.get("given_name")
        user_data["last_name"] = data.get("family_name")
        user_data["device"] = data["device"]
        return user_data

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = register_social_user(
            **self.map_user_data(serializer.validated_data)
        )
        return Response(result, status=status.HTTP_201_CREATED)


class LogInView(TokenObtainPairView):
    authentication_classes = []
    serializer_class = LogInSerializer


class RegisterView(CreateAPIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = get_user_model().objects.register_user(
            serializer.validated_data
        )
        return Response(response_data, status=status.HTTP_201_CREATED)


class ConfirmEmailRegistrationView(CreateAPIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(
            serializer.validated_data, status=status.HTTP_201_CREATED
        )


class ForgotPasswordView(GenericAPIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        instance = get_object_or_404(
            get_user_model(), email=validated_data["email"]
        )
        code = get_user_model().generate_code()
        get_user_model().set_cache(str(instance.email), code)
        subject = "Verification code"
        message = render_to_string(
            "account/email.html",
            {"code": code, "message": "Your reset password code is "},
        )
        send_email.delay(instance.email, subject, message)
        return Response(serializer.validated_data)


class VerifyResetPasswordView(GenericAPIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = ForgotPasswordVerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        instance = get_object_or_404(
            get_user_model(), email=validated_data["email"]
        )
        cache_code = cache.get(instance.email)
        if cache_code != validated_data["code"]:
            raise ValidationError("Code expired or invalid")
        guid = uuid.uuid4()
        get_user_model().set_cache(key=guid, val=instance.email, ttl=86400)
        return Response(
            data={"verification_key": guid}, status=status.HTTP_201_CREATED
        )


class ResetPasswordView(GenericAPIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = cache.get(data["verification_key"])
        if email is None:
            raise ValidationError("Guid expired or invalid")
        instance = get_user_model().objects.get(email=email)
        instance.set_password(data["password"])
        instance.save()
        return Response(status=status.HTTP_201_CREATED)


class LogOutView(APIView):
    def post(self, request):
        serializer = LogOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            device = serializer.data.get("device")
            user = request.user
            if device in user.devices:
                user.devices.remove(device)
                user.save()
            data = {
                "type": "SUCCESS",
                "info": {"message": "User successfully logged out"},
            }
            return Response(data, status=status.HTTP_200_OK)
        except TokenError:
            raise ValidationError("Token is blacklisted")


class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        instance = self.request.user
        instance.set_password(serializer.validated_data["password"])
        instance.save()
        return Response(status=status.HTTP_201_CREATED)


class UserViewSet(GenericViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    @action(methods=["PUT", "PATCH"], detail=False, url_path="update-profile")
    def update_profile(self, request):
        user = self.request.user
        serializer = self.serializer_class(
            instance=user,
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=["GET"], detail=False, url_path="get-profile")
    def get_profile(self, request):
        serializer = self.serializer_class(
            request.user, context=self.get_serializer_context()
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["PUT"], detail=False, url_path="update-notification-settings"
    )
    def update_notification_settings(self, request):
        user = self.request.user
        data = request.data
        user.update_notification_settings(data)
        return Response(data)

    @action(
        methods=["GET"], detail=False, url_path="list-notification-settings"
    )
    def list_notification_settings(self, request):
        return Response(request.user.get_notification_settings())
