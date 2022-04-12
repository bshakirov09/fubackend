from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from fitness.core.serializers import VersionControlSerializer

from .models import VersionControl


class VersionControlView(CreateAPIView):
    serializer_class = VersionControlSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = serializer.validated_data.get("page")
        detail_id = serializer.validated_data.get("detail_id")
        version, _ = VersionControl.objects.get_or_create(
            page=page, detail_id=detail_id
        )
        return Response({"version": version.version})
