from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from fitness.core.models import BaseModel
from fitness.notification import constants
from fitness.notification.managers import NotificationManager
from fitness.websocket.utils import send_data_to_channel


class Notification(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending"
        SENT = "sent"
        READ = "read"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notifications",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=512, null=True, blank=True)
    message = models.TextField()
    status = models.CharField(
        choices=Status.choices, default=Status.PENDING, max_length=15
    )
    notification_type = models.CharField(
        choices=constants.NotificationType.choices,
        max_length=30,
        default=Status.PENDING,
    )
    additional_data = models.JSONField(blank=True, default=dict)
    is_read = models.BooleanField(default=False)
    objects = NotificationManager()


@receiver([post_save], sender=Notification)
def push_notification_devices(instance, created=False, **kwargs):
    if (
        created
        and instance.notification_type
        in instance.recipient.notification_settings
    ):
        send_data_to_channel(
            instance.recipient.id,
            "notification",
            {},
        )
