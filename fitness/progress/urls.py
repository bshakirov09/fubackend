from django.urls import include, path
from rest_framework import routers

from fitness.progress import views
from fitness.progress.views import (
    CalculateMacronutrientIntakeView,
    CalculatorRMRView,
)

router = routers.DefaultRouter()
router.register(r"weight", views.WeightViewSet, basename="weight")
router.register(r"photo", views.PhotoViewSet, basename="photo")
router.register(r"journal", views.JournalViewSet, basename="journal")

urlpatterns = [
    path("", include(router.urls)),
    path("calculate-rmr/", CalculatorRMRView.as_view(), name="calculate-rmr"),
    path(
        "calculate-macronutrient-intake/",
        CalculateMacronutrientIntakeView.as_view(),
        name="calculate-macronutrient-intake",
    ),
]
