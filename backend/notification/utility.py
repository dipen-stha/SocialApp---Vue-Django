from posts.models import Post
from friends.models import FriendRequests
from .models import Notification

def create_notification(request, type, post_id=None, friendrequest_id=None):
    created_for = None
    if type == 'post_like':
        body = f'{request.user.name} like one of your posts!'
        post = Post.objects.get(id=post_id)
        created_for = post.created_by
    elif type == 'post_comment':
        body = f'{request.user.name} commented on one of your posts!'
        post = Post.objects.get(id=post_id)
        created_for = post.created_by
    elif type == 'friend_request':
        body = f'{request.user.name} sent you a friend request!'
        friend_request = FriendRequests.objects.get(id=friendrequest_id)
        created_for = friend_request.created_for
    elif type == 'friend_request_accepted':
        body = f'{request.user.name} accepted your friend request!'
        friend_request = FriendRequests.objects.get(id=friendrequest_id)
        created_for = friend_request.created_by

    notification = Notification.objects.create(
        body = body,
        notification_type=type,
        created_by = request.user,
        post_id = post_id,
        created_for = created_for
    )

    return notification