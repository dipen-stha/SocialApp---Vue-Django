from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer

# Create your views here.
class ConversationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(users__in=[self.request.user.id,])


class ConversationDetailViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationDetailSerializer

    def get_queryset(self):
        return Conversation.objects.filter(users__in=[self.request.user.id,]).get(id=self.kwargs.get('pk'))


class ConversationMessageViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationMessageSerializer

    def get_queryset(self):
        return ConversationMessage.objects.filter(conversation__users__in=[self.request.user])

