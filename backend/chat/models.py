from django.db import models

from account.models import User
from posts.utils import format_time

# Create your models here.
class Conversation(models.Model):
    users = models.ManyToManyField(User, related_name='conversations')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Chat between {[user.name for user in self.users.all()]}'

    @property
    def formatted_modified_at(self):
        return format_time(self.modified_at)



class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_to = models.ForeignKey(User, related_name='receivers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='senders', on_delete=models.CASCADE) 

    def __str__(self):
        return f'Message from {self.created_by.name} to {self.sent_to.name}'
    
    @property
    def formatted_created_at(self):
        return format_time(self.created_at)