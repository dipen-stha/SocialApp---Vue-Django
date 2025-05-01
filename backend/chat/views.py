from django.shortcuts import render
from django.db.models import Prefetch, Q, F, Max, OuterRef, Subquery
from drf_spectacular.utils import extend_schema

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
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


class ConversationListCreateAPI(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        conversation_subquery = ConversationMessage.objects.filter(
            conversation=OuterRef('pk')
        ).order_by('-created_at')
        return Conversation.objects.filter(users__in=[self.request.user.id]).annotate(
            latest_message=Subquery(conversation_subquery.values('message'))
        )


class ConversationRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer


class ConversationMessageListCreate(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationMessageSerializer

    def get_queryset(self):
        return ConversationMessage.objects.filter(conversation__users__in=[self.request.user]).select_related().prefetch_related('conversation__users')


class ConversationMessageRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationMessageSerializer

