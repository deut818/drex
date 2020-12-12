from rest_framework import generics

from .serializers import ThreadSerializer, ChatMessageSerializer
from chat.models import Thread, ChatMessage

class ThreadRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ThreadSerializer

    def get_queryset(self):
        return Thread.objects.all()

class ChatMessageRUDView(generics.ListCreateAPIView):
    # lookup_field = 'thread'
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        return ChatMessage.objects.all()

        