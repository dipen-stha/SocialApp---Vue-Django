from django.shortcuts import render
from django.db.models import Prefetch, Q, F, Max

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
    #
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     user_messages = ConversationMessage.objects.filter(conversation__in=queryset).values('conversation').annotate(latest_id=Max('id')).values('latest_id')
    #     convo = ConversationMessage.objects.filter(id__in=user_messages)



class ConversationDetailViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationDetailSerializer

    def get_queryset(self):
        return Conversation.objects.filter(users__in=[self.request.user.id,]).get(id=self.kwargs.get('pk'))


class ConversationMessageViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationMessageSerializer

    def get_queryset(self):
        return ConversationMessage.objects.filter(conversation__users__in=[self.request.user]).select_related().prefetch_related('conversation__users')

