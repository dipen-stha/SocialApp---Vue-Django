from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.db import transaction

from account.models import CustomerUser, Email
from account.tasks import send_verification_email
from account.utils import generate_token
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

    def get_fields(self):
        fields = super().get_fields()
        if self.context.get('request') and self.context.get('request').method == 'GET':
            fields['email'] = serializers.CharField(source='email.email')
        return fields

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

    def validate_email(self, email):
        if Email.objects.filter(email=email):
            raise ValidationError("This email is already registered!")
        return email

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken!")
        return username

    def create(self, validated_data):
        try:
            with transaction.atomic():
                email = Email.objects.create(
                    email=validated_data.get('email'),
                    verification_token=generate_token(),

                )
                user = User.objects.create_user(
                    email = email,
                    name = validated_data['name'],
                    password = validated_data['password'],
                )
                customer_user = CustomerUser.objects.create(
                    user=user,
                )
        except IntegrityError as e:
            raise ValidationError({'message': "User with these credentials already exists."})
        send_verification_email.delay(user.id, user.email.email)
        return user


class UserSerializer(DynamicFieldsModelSerializer):
    friends_count = serializers.SerializerMethodField()
    is_friend = serializers.BooleanField(default=False)
    is_verified = serializers.BooleanField(source='email.is_verified')
    # friends = FriendListSerializer(many=True)

    class Meta:
        model = User
        fields = ['id','email', 'name', 'avatar', 'is_verified', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'friends_count', 'is_friend']

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