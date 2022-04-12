import os

from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from fitness.document.models import ImageModel, VideoModel
from fitness.document.serializers import (
    ImageModelSerializer,
    VideoModelSerializer,
)
from fitness.document.tasks import create_thumbnail_images


class UploadImageViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    serializer_class = ImageModelSerializer
    queryset = ImageModel.objects.all().order_by("-created_dttm")

    def create(self, request, *args, **kwargs):
        image_type = request.data.get("image_type")
        error_list = list()
        if image_type is None:
            error_list.append("image_type is required")
        if request.FILES and request.FILES.getlist("images"):
            objs = list()
            for file in request.FILES.getlist("images"):
                ct = os.path.splitext(file.name.lower())[1]
                if ct not in (".jpg", ".jpeg", ".png"):
                    raise ValidationError(
                        "available format (.jpg, .jpeg, .png)"
                    )
                image = ImageModel(file=file)
                if image_type:
                    image.image_type = image_type
                objs.append(image)
            images = ImageModel.objects.bulk_create(objs)
            serializer = self.serializer_class(images, many=True)
            obj_ids = [i.id for i in images]
            create_thumbnail_images.delay(obj_ids)
            return Response(serializer.data)
        error_list.append("images can not be null")
        if error_list:
            raise ValidationError(error_list)


class UploadVideoViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    serializer_class = VideoModelSerializer
    queryset = VideoModel.objects.all().order_by("-created_dttm")

    def create(self, request, *args, **kwargs):
        image_type = request.data.get("image_type")
        error_list = list()
        if image_type is None:
            error_list.append("image_type is required")
        if request.FILES and request.FILES.getlist("videos"):
            objs = list()
            for file in request.FILES.getlist("videos"):
                ct = os.path.splitext(file.name.lower())[1]
                if ct not in (".mp4", ".mov", ".wmv", ".avi", ".mkv"):
                    raise ValidationError(
                        "available format (.jpg, .jpeg, .png)"
                    )
                video = VideoModel(file=file)
                if image_type:
                    video.image_type = image_type
                objs.append(video)
            videos = VideoModel.objects.bulk_create(objs)
            serializer = self.serializer_class(videos, many=True)
            return Response(serializer.data)
        error_list.append("images can not be null")
        if error_list:
            raise ValidationError(error_list)
