from django.shortcuts import render

from asgiref.sync import async_to_sync

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from channels.layers import get_channel_layer

from notification.utility import create_notification

from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.
class CreateNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            post_id = request.data.get('post_id', None)
            friendrequest_id = request.data.get('friendreqeuest', None)
            type = request.data.get('notification_type')

            create_notification(request, type, post_id, friendrequest_id)

            return Response({'detail': 'Notification Sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "There was something wrong"}, exception=e, status=status.HTTP_400_BAD_REQUEST)


class NotificationCountView(APIView):
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return Notification.objects.filter(created_for=self.request.user)
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = {
            "unread_notifications": queryset.filter(is_read=False).count()
        }

        return Response({
            "data": data,
            "message": "Response received successfully."
        }, status=status.HTTP_200_OK)
    

class ListNotificationView(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(created_for=self.request.user)