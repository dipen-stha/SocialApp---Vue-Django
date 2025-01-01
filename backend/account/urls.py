from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import SignupView, UserViewSet, FriendRequestsViewSet, FriendsViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename="user")
router.register(r'friend-requests', FriendRequestsViewSet, basename='friends_requests'),

urlpatterns =[
    path('account/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/signup/', SignupView.as_view(), name='signup'),
    path('friends/<str:id>/', FriendsViewSet.as_view(), name="friends")
]

urlpatterns += router.urls