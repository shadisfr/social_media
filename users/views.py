from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from .models import CustomUser
from .serializers import UserRegisterSerializer, UserSerializer, FollowStatusSerializer
from notifications.models import Notification  

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowStatusSerializer

    @extend_schema(
        summary="Follow a user",
        description="Allows an authenticated user to follow another user.",
        request=None,
        responses={200: FollowStatusSerializer},
    )
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)

        if request.user.following.filter(id=user_id).exists():
            return Response({"message": "You are already following this user."}, status=400)

        request.user.following.add(user_to_follow)  

        Notification.objects.create(
            user=user_to_follow,
            sender=request.user,
            notification_type="follow",
        )

        return Response({"message": f"You are now following {user_to_follow.username}."})


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowStatusSerializer
    @extend_schema(
        summary="Unfollow a user",
        description="Allows an authenticated user to unfollow another user.",
        request = None,
        responses={200: FollowStatusSerializer},
    )
    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        request.user.following.remove(user_to_unfollow)
        return Response({"message": f"You have unfollowed {user_to_unfollow.username}."})

class FollowersListView(generics.ListAPIView):
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(CustomUser, id=user_id)
        return user.followers.all()

    @extend_schema(
        summary="List followers",
        description="Retrieves a list of users who follow the specified user.",
        responses={200: UserSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class FollowingListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(CustomUser, id=user_id)
        return user.following.all()

    @extend_schema(
        summary="List following users",
        description="Retrieves a list of users the specified user is following.",
        responses={200: UserSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
