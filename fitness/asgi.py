import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from fitness.websocket.routings import websocket_urlpatterns  # noqa
from fitness.websocket.socket_authentication import TokenAuthMiddleware  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fitness.settings.development")

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": TokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
