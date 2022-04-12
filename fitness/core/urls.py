from django.urls import path

from fitness.core.views import VersionControlView

urlpatterns = [path("version/", VersionControlView.as_view(), name="version")]
