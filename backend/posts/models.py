import uuid

from django.db import models
from django.utils.timesince import timesince

from account.models import User

# Create your models here.

class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts_attachments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)

    attachments = models.ManyToManyField(PostAttachment,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def created_at_formatted(self):
        time = timesince(self.created_at)
        return time.split(',')[0]