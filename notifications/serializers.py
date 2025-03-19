from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "user", "sender", "sender_username", "notification_type", "post", "timestamp", "is_read"]


class NotificationStatusSerializer(serializers.Serializer):
    message = serializers.CharField()

