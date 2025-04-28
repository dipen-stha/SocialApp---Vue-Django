from django.contrib import admin

from friends.models import FriendRequests, Friend
from friends.serializers import FriendRequestsSerializer

# Register your models here.
admin.site.register(FriendRequests)
admin.site.register(Friend)