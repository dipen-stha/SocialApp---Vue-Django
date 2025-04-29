from django.urls import path

from rest_framework.routers import DefaultRouter

from friends.views import  FriendRequestsViewSet, FriendsListAPI

router = DefaultRouter()
router.register(r'friend-requests', FriendRequestsViewSet, basename='friends_requests'),

urlpatterns = [
    path('list/<str:id>/', FriendsListAPI.as_view(), name="friends")
]