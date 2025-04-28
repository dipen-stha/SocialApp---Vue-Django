from django.shortcuts import render

from asgiref.sync import async_to_sync

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from channels.layers import get_channel_layer

from notification.utility import create_notification

from .models import Notification
from .serializers import NotificationSerializer, NotificationCountSerializer

# Create your views here.
class CreateNotificationView(CreateAPIView):
    serializer_class = NotificationSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            if not serializer_class.is_valid():
                return Response({"error": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer_class.validated_data
            post = validated_data.get('post')
            friend_request= validated_data.get('friend_request')

            create_notification(request, type, post, friend_request)

            return Response({'detail': 'Notification Sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "There was something wrong"}, exception=e, status=status.HTTP_400_BAD_REQUEST)


class NotificationStatsView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = NotificationCountSerializer

    def get(self, request, *args, **kwargs):
        notification_queryset = Notification.objects.filter(created_for=request.user, is_read=False)
        data = {
            "unread_notifications": notification_queryset.count(),
        }
        stats_serializer = NotificationCountSerializer(data=data)
        stats_serializer.is_valid(raise_exception=True)
        return Response(stats_serializer.data, status=status.HTTP_200_OK)
    

class ListNotificationView(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(created_for=self.request.user)