import json

import channels
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from fitness.notification.models import Notification


class Consumer(AsyncJsonWebsocketConsumer):
    group_name = None

    async def websocket_connect(self, event):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.group_name = f"channel_{self.scope['user'].id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name,
            )
            await self.accept()
            data, qs = await self.get_new_notification_info(self.scope)
            await self.send_json(data)
            await self.update_sent_notifications(qs)

    async def websocket_disconnect(self, message):
        if self.group_name:
            await self.channel_layer.group_discard(
                self.group_name, self.channel_name
            )
        await self.close()
        raise channels.exceptions.StopConsumer()

    async def websocket_receive(self, event):
        data = json.loads(event["text"])
        await self.send_json(data)

    async def subscription(self, event):
        await self.send_json(event["data"])

    async def notification(self, event):
        data, qs = await self.get_new_notification_info(self.scope)
        await self.send_json(data)
        await self.update_sent_notifications(qs)

    @database_sync_to_async
    def get_new_notification_info(self, scope):
        new_notification_qs = (
            scope["user"]
            .notifications.filter(status=Notification.Status.PENDING)
            .order_by("created_dttm")
        )

        new_notifications = [
            {
                "id": note.id,
                "title": note.title,
                "message": note.message,
                "additional_data": note.additional_data,
                "notification_type": note.notification_type,
                "status": note.status,
                "created_at": note.created_dttm.isoformat(),
            }
            for note in new_notification_qs
            if note.notification_type in note.recipient.notification_settings
        ]
        old_notification = [
            {
                "id": note.id,
                "title": note.title,
                "message": note.message,
                "additional_data": note.additional_data,
                "notification_type": note.notification_type,
                "status": note.status,
                "created_at": note.created_dttm.isoformat(),
            }
            for note in scope["user"]
            .notifications.filter(status=Notification.Status.SENT)
            .order_by("created_dttm")
            if note.notification_type in note.recipient.notification_settings
        ]
        message = {
            "new_notification_count": len(new_notifications),
            "old_notification_count": len(old_notification),
            "new_notifications": new_notifications,
            "old_notifications": old_notification[:5],
        }
        data = {"type": "notification", "message": message}
        return data, new_notification_qs

    @database_sync_to_async
    def update_sent_notifications(self, qs):
        qs.update(status=Notification.Status.SENT)
