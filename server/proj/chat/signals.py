from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

import chat


def send_messages(instance):
    users_id = instance.room.collocutors.all()
    tmessage = chat.serializers.MessagesSerializer(instance)
    channel_layer_push = get_channel_layer('push')
    channel_layer_chat = get_channel_layer('chat')
    for i in users_id:
        print(i.user_id)
        try:
            async_to_sync(channel_layer_chat.group_send)(
                str(i.user_id),
                {
                    "type": "chat.message",
                    "event": tmessage.data
                },
            )
            async_to_sync(channel_layer_push.group_send)(
                str(i.user_id),
                {
                    "type": "push.message",
                    "push_reason": "chat_update"
                },
            )
        except:
            pass


