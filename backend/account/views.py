from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Count

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import UserSerializer, UserSignUpSerializer, FriendRequestsSerializer
from .models import FriendRequests

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
            return User.objects.exclude(id=self.request.user.id).annotate(post_count=Count('posts')).order_by('-post_count').distinct()[:4]
        return User.objects.filter(id=self.request.user.id)
    

class FriendRequestsViewSet(ModelViewSet):
    serializer_class = FriendRequestsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FriendRequests.objects.filter(created_for=self.request.user.id)
    
    def list(self, request, *args, **kwargs):
        sent_queryset = self.get_queryset().filter(status='sent')
        friends_queryset = User.objects.get(id=request.user.id).friends.all()

        sent_serializer = FriendRequestsSerializer(sent_queryset, many=True, context={'request': request})
        accepted_serialzier = UserSerializer(friends_queryset, many=True, context={'request': request})
        return Response({
            'sent': sent_serializer.data,
            'accepted': accepted_serialzier.data
        })

    
    @action(detail=False, methods=['get'])
    def get_friends(self, request, *args, **kwargs):
        friends = User.objects.get(id=request.query_params.get('id')).friends.all()
        friends_serializer = UserSerializer(friends, many=True, context={'request': request})
        return Response({
            'friends': friends_serializer.data
        })

    
    @action(detail=True, methods=['put'])
    def update_status(self, request, *args, **kwargs):
        status = request.query_params.get('status')
        obj = self.get_object()
        obj.status = status
        user = request.user
        obj.save()
        user.friends.add(obj.created_by)
        user.save()

        return Response(FriendRequestsSerializer(obj).data)
