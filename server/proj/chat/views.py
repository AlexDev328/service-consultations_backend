from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from chat.models import Message
from chat.serializers import MessagesSerializer


class MessagesViewer(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessagesSerializer

    def list(self, request, *args, **kwargs):
        room_id = kwargs.get('room_id', False)
        if room_id:
            queryset = Message.objects.filter(room_id=room_id)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
