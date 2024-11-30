from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import SignupView, UserViewSet, FriendRequestsViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename="user")
router.register(r'send-request', FriendRequestsViewSet, basename='friend_request'),

urlpatterns =[
    path('account/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/signup/', SignupView.as_view(), name='signup'),
]

urlpatterns += router.urls