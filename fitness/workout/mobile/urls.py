from django.urls import include, path
from rest_framework import routers

from fitness.workout.mobile import views

router = routers.DefaultRouter()
router.register(r"quad-track", views.QuadTrackViewSet, basename="quad_track")
router.register(r"gym-track", views.GymTrackViewSet, basename="gym_track")

urlpatterns = [
    path("", views.WorkoutListView.as_view(), name="workout"),
    path("", include(router.urls)),
    path(
        "workout-type/<int:id>/",
        views.WorkoutTypeDetailView.as_view(),
        name="workout-type",
    ),
    path("roadmap/", views.RoadMapView.as_view(), name="roadmap"),
    path(
        "gym-detail/<int:id>/",
        views.GymRetrieveView.as_view(),
        name="gym_detail",
    ),
    path(
        "quad-detail/<int:id>/",
        views.QuadRetrieveView.as_view(),
        name="gym_detail",
    ),
]
