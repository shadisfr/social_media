from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from .models import Notification
from .serializers import NotificationSerializer, NotificationStatusSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False).order_by("-timestamp")  # ✅ Show only unread notifications


class MarkNotificationAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationStatusSerializer

    @extend_schema(
        summary="Mark notification as read",
        description="Marks a specific notification as read.",
        request=None,
        responses={200: NotificationStatusSerializer},
    )
    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read"})
