# Generated by Django 5.1.3 on 2024-12-26 15:45

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0006_alter_comment_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_read', models.BooleanField(default=False)),
                ('notification_type', models.CharField(choices=[('friend_request', 'Friend Request'), ('friend_request_accepted', 'Friend Request Accepted'), ('post_like', 'Post Like'), ('post_comment', 'Post Comment')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_notifications', to=settings.AUTH_USER_MODEL)),
                ('created_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_notifications', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
    ]