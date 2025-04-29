from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.db import transaction

from account.models import CustomerUser
from commons.serializers import DynamicFieldsModelSerializer

User = get_user_model()


class UserSignUpSerializer(ModelSerializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'repeat_password']

    def validate(self, data):
        password = data['password']
        repeat_password = data['repeat_password']
        if password != repeat_password:
            raise serializers.ValidationError(
                {
                'password': 'Passwords do not match',
                'repeat_password': 'Passwords do not match'
                }
            )
        return data

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(
                email = validated_data['email'],
                name = validated_data['name'],
                password = validated_data['password'],
            )
            customer_user = CustomerUser.objects.create(
                user=user,
            )
        return user


class UserSerializer(DynamicFieldsModelSerializer):
    friends_count = serializers.SerializerMethodField()
    # friends = FriendListSerializer(many=True)

    class Meta:
        model = User
        fields = ['id','email', 'name', 'avatar', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'friends_count']

    def get_friends_count(self, instance) -> int:
        return instance.friends.count()


class UserSearchSerializer(ModelSerializer):
    post_count = serializers.IntegerField()
    friends_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','email', 'name', 'avatar', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'post_count', 'friends_count']

    def get_friends_count(self, instance):
        return instance.friends.count()


class UserStatsSerializer(serializers.ModelSerializer):
    friends_count = serializers.CharField()
    posts_count = serializers.CharField()

    class Meta:
        model = User
        fields = ['friends_count', 'posts_count']