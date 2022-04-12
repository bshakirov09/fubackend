import logging
from datetime import datetime

import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from django.utils.timezone import is_naive, make_aware, utc


def make_utc(dt):
    if settings.USE_TZ and is_naive(dt):
        return make_aware(dt, timezone=utc)
    return dt


def datetime_from_epoch(ts):
    return make_utc(datetime.utcfromtimestamp(ts))


@database_sync_to_async
def get_user(token):
    close_old_connections()
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        claim_time = datetime_from_epoch(decoded["exp"])
        if claim_time <= datetime.now():
            return AnonymousUser()
        if decoded["token_type"] != "access":
            return AnonymousUser()
        user = get_user_model().objects.get(id=decoded["user_id"])
        return user
    except Exception as e:
        logging.warning(e)
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        if b"authorization" in headers:
            try:

                token_key = headers[b"authorization"].decode("utf8").split()[1]
            except ValueError:
                token_key = None
            scope["user"] = (
                AnonymousUser()
                if token_key is None
                else await get_user(token_key)
            )
        else:
            scope["user"] = AnonymousUser()
        return await super().__call__(scope, receive, send)
