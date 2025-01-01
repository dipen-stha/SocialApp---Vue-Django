import uuid

from django.db import models

from account.models import User
from posts.models import Post

# Create your models here.
class Notification(models.Model):
    FRIEND_REQUEST = 'friend_request'
    FRIEND_REQUEST_ACCEPTED = 'friend_request_accepted'
    POST_LIKE = 'post_like'
    POST_COMMENT = 'post_comment'

    NOTIFICATION_TYPES = [
        (FRIEND_REQUEST, 'Friend Request'),
        (FRIEND_REQUEST_ACCEPTED, 'Friend Request Accepted'),
        (POST_LIKE, 'Post Like'),
        (POST_COMMENT, 'Post Comment'),
    ]

    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='created_notifications', on_delete=models.CASCADE) 
    created_for = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.notification_type} Notification for {self.created_for.name}'