from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import FriendRequests

User = get_user_model()


class UserSignUpSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password'],
        )
        return user


class UserSerializer(ModelSerializer):
    friends_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','email', 'name', 'avatar', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'friends_count', 'friends']

    def get_friends_count(self, instance):
        return instance.friends.count()

class UserSearchSerializer(ModelSerializer):
    post_count = serializers.IntegerField()
    friends_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','email', 'name', 'avatar', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'post_count', 'friends_count']

    def get_friends_count(self, instance):
        return instance.friends.count()


class FriendRequestsSerializer(ModelSerializer):
    created_for = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequests
        fields = ['id', 'created_for', 'status', 'created_at', 'created_by']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['created_by'] = request.user
        created_for_instance = get_object_or_404(User, id=request.query_params.get('user'))
        validated_data['created_for'] = created_for_instance
        instance = FriendRequests.objects.get_or_create(**validated_data)
        return instance