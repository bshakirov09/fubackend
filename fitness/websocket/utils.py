import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from psycopg2.extensions import JSON


def send_data_to_channel(
    user_id: int, message_type: str, message: JSON
) -> tuple:
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"channel_{user_id}",
            {
                "type": message_type,
                "data": {"type": message_type, "message": message},
            },
        )
    except Exception as e:
        logging.warning(f"{e}")
