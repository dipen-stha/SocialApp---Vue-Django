from django.urls import path

from .views import CreateNotificationView, NotificationCountView, ListNotificationView

urlpatterns = [
    path('create/', CreateNotificationView.as_view(), name='create'),
    path('get_count/', NotificationCountView.as_view(), name='get-count'),
    path('list_notifications/', ListNotificationView.as_view(), name='list-notifications'),
]
