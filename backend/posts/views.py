from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db.models import Q, Count
from django.shortcuts import get_object_or_404

from .models import Post, PostAttachment, Like, Comment
from .serializers import PostAttachmentSerializers, PostSerializer, LikeSerializer, CommentSerializer
from account.models import User
from account.serializers import UserSerializer, UserSearchSerializer


# Create your views here.
class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.query_params.get('user'):
            return Post.objects.filter(created_by_id=self.request.query_params.get('user')).select_related('created_by').prefetch_related('attachments')
        return Post.objects.select_related('created_by').prefetch_related('attachments').filter(Q(created_by=self.request.user))
    
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user_id = request.query_params.get('user', None)
        posts_serializer = self.serializer_class(queryset, many=True, context={'request': request})
        if user_id:
            user = User.objects.get(id=request.query_params.get('user'))
            user_serializer = UserSerializer(user, context={'request': request})

        return Response({
            'posts': posts_serializer.data,
            'user': user_serializer.data if user_id else None
        })
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        search_query = request.query_params.get('q', '')

        if not search_query:
            return Response({'error': 'Nothing to search'})
        
        user_queryset = User.objects.filter(name__icontains=search_query
        ).annotate(
            post_count=Count('posts'))

        posts_queryset = Post.objects.filter(
        body__icontains=search_query
        )

        user_serializer = UserSearchSerializer(user_queryset, many=True, context={'request':request})

        posts_serializer = PostSerializer(posts_queryset, many=True, context={'request':request})

        return Response({
            "user": user_serializer.data,
            "posts": posts_serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def add_likes(self, request, *args, **kwargs):
        data = {
            'post': get_object_or_404(Post, id=kwargs.get('pk'))
        }
        like_serializer = LikeSerializer(data=data, context={'request': request})
        if like_serializer.is_valid():
            like_instance = like_serializer.save()
            return Response({
                'likes': LikeSerializer(like_instance).data
            })
        return Response({
            'error': 'There was an error.'
        })
    
    @action(detail=True, methods=['post'])
    def add_comments(self, request, *args, **kwargs):
        request.data['post_id'] = kwargs.get('pk')

        comment_serializer = CommentSerializer(data=request.data, context=
        {'request': request})
        if comment_serializer.is_valid():
            comment_serializer.save()
        return Response({
            'comment': comment_serializer.data
        })
            