from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from fitness.core.pagination import Pagination
from fitness.notification.models import Notification
from fitness.notification.serializers import (
    NotificationListUpdateSerializer,
    NotificationSerializer,
)


class ListNotification(ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return Notification.objects.get_user_notifications(self.request.user)


class NotificationListUpdateView(UpdateAPIView):
    serializer_class = NotificationListUpdateSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Notification.objects.update_status_to_read(serializer.validated_data)
        return Response(serializer.data)


class NotificationStatusUpdate(APIView):
    def put(self, request, *args, **kwargs):
        Notification.objects.filter(recipient=request.user).update(
            status=Notification.Status.READ
        )
        return Response(status=status.HTTP_200_OK)
