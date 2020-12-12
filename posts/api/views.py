from rest_framework import generics
from django.db.models import Q

from posts.models import Post
from .serializers import PostSerializer
class PostsRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = PostSerializer
    # queryset = Post.objects.all()

    def get_queryset(self):
        return Post.objects.all()

class PostsAPIView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = Post.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(Q(title__icontains=query))
        return qs
