from django.urls import include, path
from rest_framework import routers

from fitness.blog import views

router = routers.DefaultRouter()

router.register(r"blog", views.BlogViewSet, basename="blog")
router.register(
    r"blog-images", views.BlogImagesViewSet, basename="blog-images"
)

urlpatterns = [
    path("", include(router.urls)),
]
