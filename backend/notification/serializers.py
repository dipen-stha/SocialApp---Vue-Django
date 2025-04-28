from rest_framework import serializers

from posts.serializers import PostSerializer
from .models import Notification
from account.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(fields=('id', 'avatar'), read_only=True)
    type = serializers.CharField(max_length=50, write_only=True)
    friend_request = serializers.IntegerField(write_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'created_by', 'body', 'is_read', 'post', 'type', 'friend_request']

    def get_fields(self):
        fields = super(NotificationSerializer, self).get_fields()
        if self.context.get('request') and self.context.get('request').method == 'GET':
            fields['post'] = PostSerializer(read_only=True)
        return fields


class NotificationCountSerializer(serializers.Serializer):
    # message_count = serializers.CharField()
    unread_notification_count = serializers.CharField(read_only=True)