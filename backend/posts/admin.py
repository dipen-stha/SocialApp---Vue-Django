from django.contrib import admin
from .models import Post, PostAttachment, Like, Comment
# Register your models here.
admin.site.register(PostAttachment)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)