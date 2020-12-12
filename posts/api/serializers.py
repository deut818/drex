from rest_framework import serializers

from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['pk', 'user', 'title', 'slug', 'url', 'image', 'video', 'users_like', 'total_likes', 'created']
        read_only_fields = ['pk',]
        