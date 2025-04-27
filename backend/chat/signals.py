from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from . models import ConversationMessage

@receiver(post_save, sender=ConversationMessage)
def message_create(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_group',
            {
                "type": "chat_message",
                "data": instance
            }
        )