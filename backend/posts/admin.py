from django.contrib import admin
from .models import Post, PostAttachment
# Register your models here.
admin.site.register(PostAttachment)
admin.site.register(Post)