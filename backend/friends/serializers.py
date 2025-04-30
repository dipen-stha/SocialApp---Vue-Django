from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from commons.serializers import DynamicFieldsModelSerializer
from .models import FriendRequests, Friend
from account.models import User
from account.serializers import UserSerializer



class FriendListSerializer(ModelSerializer):

    class Meta:
        model = Friend
        fields = ['friend','user']


class FriendRequestsSerializer(ModelSerializer):
    created_by = UserSerializer(fields=['id', 'avatar'], read_only=True)

    class Meta:
        model = FriendRequests
        fields = ['id', 'created_for', 'status', 'created_at', 'created_by']

    def get_fields(self):
        fields = super().get_fields()
        if self.context['request'] and self.context['request'].method == "GET":
            fields['created_for'] = UserSerializer(fields=['id', 'avatar'], read_only=True)
        return fields

    def create(self, validated_data):
        request = self.context['request']
        validated_data['created_by'] = request.user
        instance, _ = FriendRequests.objects.get_or_create(**validated_data)
        return instance

    def validate_status(self, value):
        if self.instance.status.lower() == value:
            raise ValidationError(f"Status is already {value}")
        return value


class FriendSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    friend = UserSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ['id', 'user', 'friend']