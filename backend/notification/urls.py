from django.urls import path

from .views import CreateNotificationView, NotificationStatsView, ListNotificationView

urlpatterns = [
    path('create/', CreateNotificationView.as_view(), name='create'),
    path('get-stats/', NotificationStatsView.as_view(), name='get_stats'),
    path('list-notifications/', ListNotificationView.as_view(), name='list_notifications'),
]
