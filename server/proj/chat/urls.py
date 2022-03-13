from django.conf.urls import url
from django.urls import path

from .views import MessagesViewer

urlpatterns = [
    path('chat/<int:room_id>/', MessagesViewer.as_view({'get': 'list', 'post': 'create'})),
]
