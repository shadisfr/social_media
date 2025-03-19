from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.email")  
    receiver = serializers.ReadOnlyField(source="receiver.email")  
    
    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "content", "timestamp", "is_read"]

class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["receiver", "content"]  

class ConversationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()


class MessageStatusSerializer(serializers.Serializer):
    message = serializers.CharField()
