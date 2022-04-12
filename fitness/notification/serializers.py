from rest_framework import serializers

from fitness.notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "title",
            "message",
            "additional_data",
            "notification_type",
            "status",
            "created_dttm",
        )


class NotificationUpdateSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Notification.objects.all()
    )


class NotificationListUpdateSerializer(serializers.Serializer):
    notifications = NotificationUpdateSerializer(many=True)
