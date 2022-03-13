from django.urls import re_path

from . import consumers
from django.conf.urls import url, include

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'push/(?P<id>[0-9a-z]+)/$', consumers.PushConsumer.as_asgi()),
]