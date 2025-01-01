from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Count, Prefetch, Q
from django.db import transaction

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import UserSerializer, UserSignUpSerializer, FriendRequestsSerializer, FriendSerializer
from .models import FriendRequests, Friend

User = get_user_model()
# Create your views here.

class SignupView(CreateAPIView):
    model = User
    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        self.tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        response.data['tokens'] = self.tokens
        return response
    

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self): 
        if self.request.query_params.get('type') == 'recommendations':
            return User.objects.exclude(id=self.request.user.id).annotate(post_count=Count('posts')).order_by('-post_count').prefetch_related('friends').distinct()[:4]

        return User.objects.filter(id=self.request.user.id).prefetch_related('friends')


class FriendRequestsViewSet(ModelViewSet):
    serializer_class = FriendRequestsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FriendRequests.objects.filter(Q(created_for=self.request.user) | Q(created_by=self.request.user)).select_related('created_for', 'created_by')

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, context={"request": request}, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if instance.status == 'accepted':
                Friend.objects.create(user=instance.created_for, friend=instance.created_by)
                Friend.objects.create(user=instance.created_by, friend=instance.created_for)
        
        return Response(serializer.data)


class FriendsViewSet(ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]
    queryset = Friend.objects.select_related('user', 'friend')

    def get_queryset(self):
        return self.queryset.filter(user=self.kwargs.get('id'))