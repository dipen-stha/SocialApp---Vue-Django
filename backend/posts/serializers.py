from rest_framework import serializers
from .models import Post, PostAttachment
from account.serializers import UserSerializer

class PostAttachmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ['id', 'image', 'created_at', 'created_by']


class PostSerializer(serializers.ModelSerializer):
    attachments = PostAttachmentSerializers(many=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'body', 'created_at_formatted', 'created_by', 'attachments']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        attachments_data = validated_data.pop('attachments', None)
        instance = Post.objects.create(**validated_data)
        if attachments_data:
            for attachment in attachments_data:
                attachment_instance, _ = PostAttachment.objects.get_or_create(**attachment)
                instance.attachments.add(attachment_instance)
        return instance
            