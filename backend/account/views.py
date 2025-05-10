from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Count, Prefetch, Q, Case, When
from django.db import transaction

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from django_filters import rest_framework as filters

from .serializers import UserSerializer, UserSignUpSerializer, UserStatsSerializer

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

class SelfUserAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.GET.get('type') == 'recommendations':
            return self.queryset.exclude(
                id=self.request.user.id
            ).annotate(
                post_count=Count('posts')).order_by('-post_count').prefetch_related('friends').distinct()[:4]
        return self.queryset.annotate(
            is_friend=Case(
                When(
                    id__in=self.request.user.friends.values_list('id'),
                then=True), default=False)
        )


class UserStatsAPI(APIView):
    queryset = User.objects.all()
    serializer_class = UserStatsSerializer

    def get(self, request, id):
        queryset = self.queryset.filter(id=id).prefetch_related('friends', 'posts').aggregate(
            friends_count=Count('friends'),
            posts_count=Count('posts')
        )
        serializer_class = self.serializer_class(queryset)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
