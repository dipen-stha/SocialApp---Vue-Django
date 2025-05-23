from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import SignupView, UserViewSet, SelfUserAPIView, UserStatsAPI, VerifyEmailView

router = DefaultRouter()
router.register(r'user', UserViewSet, basename="user")
urlpatterns =[
    path('authenticate/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('authenticate/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('authenticate/signup/', SignupView.as_view(), name='signup'),
    path('authenticate/self/user/', SelfUserAPIView.as_view(), name='self'),
    path('authenticate/verify/<str:token>/', VerifyEmailView.as_view(), name='verify'),
    path('user/stats/<str:id>/', UserStatsAPI.as_view(), name='stats')
]

urlpatterns += router.urls