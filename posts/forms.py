from django import forms
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Post, Comment, CommentReply

class PostCreateForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class':'form-control post-create',
        'placeholder':"What's up ...?"
    }))
    image = forms.ImageField(label='', required=False)
    video = forms.FileField(label='', required=False)
    audio = forms.FileField(label='', required=False)

    class Meta:
        model = Post
        fields = ('title', 'image', 'video', 'audio', 'url')

class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={
        "class": "form-control comment",
        "placeholder": "Comment on this post",
    }))

    class Meta:
        model = Comment
        fields = ('body',)

class CommentReplyForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={
        "class": "form-control comment-reply",
        "placeholder": "Reply to this comment",
    }))

    class Meta:
        model = CommentReply
        fields = ('body',)
