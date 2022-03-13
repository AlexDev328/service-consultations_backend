from rest_framework import serializers

from chat.models import Room, Message


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'