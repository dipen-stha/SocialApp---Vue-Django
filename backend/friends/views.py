from django.db import transaction
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . models import Friend, FriendRequests
from .serializers import FriendSerializer, FriendRequestsSerializer

# Create your views here.


class FriendRequestsViewSet(ModelViewSet):
    serializer_class = FriendRequestsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequests.objects.filter(
            Q(created_for=self.request.user) | Q(created_by=self.request.user)).select_related('created_for',
                                                                                               'created_by')

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