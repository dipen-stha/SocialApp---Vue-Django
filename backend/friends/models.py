import uuid

from django.db import models

from account.models import User
# Create your models here.


class FriendRequests(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_for = models.ForeignKey(User, related_name="friend_requests", on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=SENT)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_friend_requests', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('created_by', 'created_for')

    def __str__(self):
        return f"Request from {self.created_by.name} to {self.created_for.name}"


class Friend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="friends", on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name="friends_of", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')
        indexes = [
            models.Index(fields=['user', 'friend'])
        ]

    def __str__(self):
        return f"{self.user.name} is friends with {self.friend.name}"