from django.urls import path, re_path, include

from .views import PostsRUDView, PostsAPIView

app_name = 'api-posts'
urlpatterns = [
    re_path(r'^(?P<pk>\d+)/$', PostsRUDView.as_view(), name='posts-rud'),
    path('', PostsAPIView.as_view(), name='posts-create'),
]