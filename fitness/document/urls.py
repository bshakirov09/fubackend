from django.urls import include, path
from rest_framework import routers

from fitness.document import views

router = routers.DefaultRouter()
router.register(r"upload-images", views.UploadImageViewSet)
router.register(r"upload-videos", views.UploadVideoViewSet)

urlpatterns = [
    path(r"document/", include(router.urls)),
]
