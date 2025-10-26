from rest_framework import serializers
from .models import ChatRoom, Message

class ChatRoomSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'created_by']
        
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()  

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'content', 'timestamp']