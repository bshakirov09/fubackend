from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from fitness.account import views

routers = routers.DefaultRouter()

routers.register(r"user", views.UserViewSet, basename="user")

urlpatterns = [
    path("logout/", views.LogOutView.as_view(), name="logout"),
    path("login/", views.LogInView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("google/", views.GoogleSocialAuthView.as_view(), name="google"),
    path("facebook/", views.FacebookSocialAuthView.as_view(), name="facebook"),
    path("apple/", views.AppleSocialAuthView.as_view(), name="apple"),
    path(
        "confirm-register/",
        views.ConfirmEmailRegistrationView.as_view(),
        name="confirm_register",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "forgot-password/verify-email/",
        views.ForgotPasswordView.as_view(),
        name="verify-email",
    ),
    path(
        "forgot-password/verify-code/",
        views.VerifyResetPasswordView.as_view(),
        name="verify-code",
    ),
    path(
        "forgot-password/reset-password/",
        views.ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path(
        "change-password/",
        views.ChangePasswordView.as_view(),
        name="change-password",
    ),
    path("", include(routers.urls)),
]
