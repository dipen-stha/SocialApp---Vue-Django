from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    ConversationViewSet,
    ConversationListCreateAPI,
    ConversationRetrieveUpdateDestroyAPI,
    ConversationMessageListCreate,
    ConversationMessageRetrieveUpdateDestroyAPI,
)

router = DefaultRouter()

router.register(r'conversation', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('conversation/', ConversationListCreateAPI.as_view(), name='conversation_list_create'),
    path('conversation/<str:pk>/', ConversationRetrieveUpdateDestroyAPI.as_view(), name='conversation_detail'),
    path('conversation-message/', ConversationMessageListCreate.as_view(), name='conversation_message_list_create'),
    path('conversation-message/<str:id>', ConversationMessageRetrieveUpdateDestroyAPI.as_view(), name='conversation_message_detail'),
]

urlpatterns += router.urls