from django.urls import include, path
from rest_framework import routers

from fitness.workout.dashboard import views

router = routers.DefaultRouter()
router.register(r"workout", views.WorkoutViewSet, basename="workout")
router.register(
    r"workout-type", views.WorkoutTypeViewSet, basename="workout-type"
)
router.register(r"gym", views.GymViewSet, basename="gym")
router.register(r"quad", views.QuadViewSet, basename="quad")

urlpatterns = [
    path("", include(router.urls)),
]
