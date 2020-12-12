from django.contrib import admin

from .models import Post, Comment, CommentReply
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'video', 'audio', 'created']
    list_filter = ['created']

@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ['user', 'post', 'body', 'created', 'updated', 'active']
    list_filter = ['created']
    search_fields = ['user', 'post']

@admin.register(CommentReply)
class Comment(admin.ModelAdmin):
    list_display = ['user', 'comment', 'body', 'created', 'active']
    list_filter = ['created']
    search_fields = ['user', 'post', 'comment']