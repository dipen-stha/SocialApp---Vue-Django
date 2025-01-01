from rest_framework import serializers

from .models import Notification
from account.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(fields=('id', 'avatar'), read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'


class NotificationCountSerializer(serializers.Serializer):
    # message_count = serializers.CharField()
    unread_notification_count = serializers.CharField(read_only=True)