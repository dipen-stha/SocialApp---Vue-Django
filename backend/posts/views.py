from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db.models import Q, Count

from .models import Post, PostAttachment
from .serializers import PostAttachmentSerializers, PostSerializer
from account.models import User
from account.serializers import UserSerializer, UserSearchSerializer


# Create your views here.
class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.query_params.get('user'):
            return Post.objects.filter(created_by_id=self.request.query_params.get('user')).select_related('created_by').prefetch_related('attachments')
        return Post.objects.select_related('created_by').prefetch_related('attachments').filter(Q(created_by=self.request.user) | Q(created_by__in=self.request.user.friends.all()))
    
        
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