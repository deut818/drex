from rest_framework import serializers

from chat.models import Thread, ChatMessage

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['pk', 'first', 'second', 'updated', 'timestamp',]

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['pk', 'thread', 'user', 'message', 'timestamp']
        read_only_fields = ['pk', 'user','thread']