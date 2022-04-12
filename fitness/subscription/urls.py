from django.urls import include, path
from rest_framework import routers

from fitness.subscription import views

routers = routers.DefaultRouter()

routers.register(
    r"subscription", views.SubscriptionViewSet, basename="subscription"
)
routers.register(
    r"user-subscription",
    views.UserSubscriptionViewSet,
    basename="user-subscription",
)

urlpatterns = [
    path("subscription/webhook/", views.SubscriptionWebhook.as_view()),
    path("", include(routers.urls)),
]
