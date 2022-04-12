from django.db import models


class NotificationManager(models.Manager):
    def get_user_notifications(self, user):
        return self.filter(
            recipient=user, notification_type__in=user.notification_settings
        ).order_by("-id")

    def update_status_to_read(self, data):
        notification_list = data.get("notifications")
        for item in notification_list:
            notification = item.get("id")
            notification.status = self.model.Status.READ
            notification.save()
