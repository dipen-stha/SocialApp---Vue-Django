from rest_framework.routers import DefaultRouter

from .views import ConversationViewSet, ConversationDetailViewSet, ConversationMessageViewSet

router = DefaultRouter()

router.register(r'conversation', ConversationViewSet, basename='conversation')
router.register(r'conversation-detail', ConversationDetailViewSet, basename='conversation_detail')
router.register(r'conversation-message', ConversationMessageViewSet, basename='conversation_message')

urlpatterns = router.urls