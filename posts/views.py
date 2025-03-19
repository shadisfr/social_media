from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer, LikeStatusSerializer
from notifications.models import Notification  
from django.shortcuts import get_object_or_404


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-created_at")  
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Create or list posts",
        description="Lists all posts or allows authenticated users to create a new post.",
        request=PostSerializer,
        responses={201: PostSerializer},
    )
    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Retrieve, update, or delete a post",
        description="Allows an authenticated user to retrieve, edit, or delete their own post.",
        responses={200: PostSerializer},
    )
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response({"error": "You can only delete your own posts."}, status=403)
        return super().delete(request, *args, **kwargs)

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeStatusSerializer
    @extend_schema(
        summary="Like or unlike a post",
        description="Toggles like status for a post.",
        request=None,
        responses={200: LikeStatusSerializer},
    )
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            like.delete()
            return Response({"message": "Unliked post."})

        Notification.objects.create(
            user=post.author,
            sender=request.user,  
            notification_type="like",
            post=post
        )
        return Response({"message": "Liked post."})

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id)

    @extend_schema(
        summary="Create or list comments",
        description="Lists comments on a post or allows users to add a comment.",
        responses={201: CommentSerializer},
    )
    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        comment = serializer.save(user=self.request.user, post_id=post_id)

        Notification.objects.create(
            user=comment.post.author,
            sender=self.request.user,
            notification_type="comment",
            post=comment.post
        )

class TimelineFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by("-created_at")
