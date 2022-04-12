from django.urls import path

from fitness.websocket import consumers

websocket_urlpatterns = [
    path("ws/", consumers.Consumer.as_asgi()),
]
