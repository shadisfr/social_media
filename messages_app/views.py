from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from .models import Message
from .serializers import MessageSerializer, SendMessageSerializer, ConversationSerializer, MessageStatusSerializer
from notifications.models import Notification  
from users.serializers import UserSerializer  
from users.models import CustomUser

class SendMessageView(generics.CreateAPIView):
    """
    API endpoint to send a new message.
    """
    serializer_class = SendMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Send a message",
        description="Allows an authenticated user to send a message to another user.",
        request=SendMessageSerializer,
        responses={201: MessageSerializer},
    )
    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user) 

        if message.receiver:
            Notification.objects.create(
                user=message.receiver,  
                sender=message.sender, 
                notification_type="message",  
            )


class ConversationListView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Get conversation with a user",
        description="Fetches all messages exchanged between the authenticated user and the specified user.",
        responses={200: MessageSerializer(many=True)},
    )
    def get(self, request, user_id):
        user = request.user
        messages = Message.objects.filter(
            Q(sender=user, receiver_id=user_id) | Q(sender_id=user_id, receiver=user)
        ).order_by("timestamp")

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=200)  




class MarkMessagesAsReadView(GenericAPIView):
    """
    API endpoint to mark messages as read from a specific user.
    """
    serializer_class = MessageStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Mark messages as read",
        description="Marks all unread messages from a specified user as read.",
        request=None,
        responses={200: MessageStatusSerializer}, 
    )
    def post(self, request, user_id):
        Message.objects.filter(sender_id=user_id, receiver=request.user, is_read=False).update(is_read=True)
        return Response({"message": "Messages marked as read."})



class ConversationList(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="List conversations",
        description="Retrieves a list of users the authenticated user has messaged.",
        responses={200: UserSerializer(many=True)},
    )
    def get(self, request):
        user = request.user
        conversations = Message.objects.filter(Q(sender=user) | Q(receiver=user)).values("sender", "receiver").distinct()

        user_ids = set()
        for convo in conversations:
            user_ids.add(convo["sender"])
            user_ids.add(convo["receiver"])

        user_ids.discard(user.id)  
        users = CustomUser.objects.filter(id__in=user_ids)  
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
