from django.urls import path

from rest_framework.routers import DefaultRouter

from friends.views import  FriendRequestsViewSet, FriendsViewSet

router = DefaultRouter()
router.register(r'friend-requests', FriendRequestsViewSet, basename='friends_requests'),

urlpatterns = [
    path('friends/<str:id>/', FriendsViewSet.as_view(), name="friends")
]