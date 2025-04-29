from django.db import IntegrityError
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db.models import Q, Count, Prefetch
from django.shortcuts import get_object_or_404

from .models import Post, PostAttachment, Like, Comment
from .serializers import PostAttachmentSerializers, PostSerializer, LikeSerializer, CommentSerializer
from account.models import User
from account.serializers import UserSerializer, UserSearchSerializer


# Create your views here.
class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.select_related('created_by').prefetch_related(
        'attachments',
        Prefetch('likes', queryset=Like.objects.select_related('created_by')),
        Prefetch('comments', queryset=Comment.objects.select_related('created_by', 'post'))
        )

    def get_queryset(self):
        if self.request.query_params.get('user'):
        #     return Post.objects.filter(created_by_id=self.request.query_params.get('user')).select_related('created_by').prefetch_related('attachments')
        # return Post.objects.select_related('created_by').prefetch_related('attachments').filter(created_by=self.request.user)
            return self.queryset.filter(created_by_id=self.request.query_params.get('user'))
        return self.queryset.filter(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        search_query = request.query_params.get('q', '')

        if not search_query:
            return Response({'message': 'Nothing to search'}, status=status.HTTP_400_BAD_REQUEST)
        
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
            'post': get_object_or_404(Post, id=kwargs.get('pk')).id
        }
        like_serializer = LikeSerializer(data=data, context={'request': request})
        if like_serializer.is_valid():
            try:
                validated_data = like_serializer.validated_data
                validated_data['created_by'] = self.request.user
                like_instance, created = Like.objects.get_or_create(**validated_data)
                if not created:
                    like_instance.delete()
                    return Response({'message': 'Post Disliked'}, status=status.HTTP_200_OK)
                return Response({
                    'likes': LikeSerializer(like_instance).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Internal Server Error - {e}"})

        return Response({
            "message": like_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
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
            