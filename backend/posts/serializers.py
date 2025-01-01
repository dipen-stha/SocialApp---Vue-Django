from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Post, PostAttachment, Like, Comment
from account.serializers import UserSerializer

class PostAttachmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ['id', 'image', 'created_at', 'created_by']


class PostSerializer(serializers.ModelSerializer):
    attachments = PostAttachmentSerializers(many=True)
    created_by = UserSerializer(fields=['id', 'name', 'avatar'],read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    created_at_formatted = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'body', 'created_at_formatted', 'created_by', 'attachments', 'likes_count', 'comments_count']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and request.method.lower() == ('get' or 'retrieve'):
            if 'likes' not in fields:
                fields['likes'] = LikeSerializer(many=True)
            if 'comments' not in fields:
                fields['comments'] = CommentSerializer(many=True)
        return fields

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        attachments_data = validated_data.pop('attachments', None)
        instance = Post.objects.create(**validated_data)
        if attachments_data:
            for attachment in attachments_data:
                attachment_instance, _ = PostAttachment.objects.get_or_create(**attachment)
                instance.attachments.add(attachment_instance)
        return instance
    

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['id', 'created_by', 'created_at', 'post']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and request.method.lower() == 'get':
            fields = {key: value for key, value in fields.items() if key != 'post'}
        return fields

    def validate(self, attrs):
        if isinstance(self.initial_data.get('post'), Post):
            attrs.update({
                'post': self.initial_data.get('post')
                })
        return attrs

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        instance, created = Like.objects.get_or_create(**validated_data)
        if not created:
            raise 
        instance.save()
        return instance
    

class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(fields=['avatar', 'name'],read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at_formatted = serializers.CharField()

    class Meta:
        model = Comment
        fields = ['id', 'body', 'post', 'created_at_formatted', 'created_by']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and request.method.lower() == 'get':
            fields = {key: value for key, value in fields.items() if key != 'post'}
        return fields

    def validate(self, attrs):
        post = get_object_or_404(Post, id=self.initial_data.get('post_id'))

        attrs.update({'post': post})
        return attrs

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        instance = Comment(**validated_data)
        instance.save()
        return instance

            