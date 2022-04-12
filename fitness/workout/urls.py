from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path("workout/mobile/", include("fitness.workout.mobile.urls")),
    path("workout/admin/", include("fitness.workout.dashboard.urls")),
]
