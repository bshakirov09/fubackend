from django.urls import include, path
from rest_framework import routers

from fitness.recipe import views

router = routers.DefaultRouter()

router.register(r"recipe", views.RecipeViewSet, basename="recipe")
router.register(
    r"recipe-category", views.CategoryViewSet, basename="recipe-category"
)
router.register(
    r"recipe-category-image",
    views.CategoryImageAdminViewSet,
    basename="recipe-category-image",
)
urlpatterns = [
    path("", include(router.urls)),
]
