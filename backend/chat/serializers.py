from rest_framework import serializers

from account.serializers import UserSerializer
from account.models import User
from .models import Conversation, ConversationMessage


class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(fields=['id', 'name', 'avatar'], many=True, read_only=True)
    formatted_modified_at = serializers.CharField()

    class Meta:
        model = Conversation
        fields = ['id', 'users', 'formatted_modified_at']

# class ConversationSerializer(serializers.ModelSerializer):
#     sent_by = UserSerializer(fields=['id', 'name', 'avatar'], read_only=True)
#     formatted_modified_at = serializers.CharField()
#     last_message = serializers.CharField(read_only=True)
#
#     class Meta:
#         model = Conversation
#         fields = ['id', 'sent_by', 'formatted_modified_at', 'last_message']


class ConversationMessageSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(fields=['id', 'name', 'avatar'], read_only=True)
    sent_to = UserSerializer(fields=['id', 'name', 'avatar'], read_only=True)
    conversation = ConversationSerializer(read_only=True)
    formatted_created_at = serializers.CharField(read_only=True)
    is_read = serializers.BooleanField(read_only=True)

    class Meta:
        model = ConversationMessage
        fields = ['id', 'created_by', 'is_read', 'sent_to', 'created_at', 'message', 'conversation', 'formatted_created_at']

    def get_fields(self):
        fields = super().get_fields()
        if self.context['request'] and self.context['request'].method.lower() == 'post':
            fields['conversation'] = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all(), write_only=True)

            fields['sent_to'] = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
        return fields
    
    def create(self, validated_data):
        # Automatically set the created_by field to the current user
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        else:
            raise serializers.ValidationError("User must be authenticated to create a message.")

        return super().create(validated_data)


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = ConversationSerializer(many=True, read_only=True)
    formatted_modified_at = serializers.CharField()

    class Meta:
        model = Conversation
        fields = ['id', 'users', 'messages', 'formatted_modified_at']