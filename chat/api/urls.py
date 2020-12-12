from django.urls import path, re_path, include

from .views import ThreadRUDView, ChatMessageRUDView

app_name = 'chat-api'
urlpatterns = [
    re_path(r'^(?P<pk>\d+)/$', ThreadRUDView.as_view(), name='threads-api'),
    re_path(r'^messages/$', ChatMessageRUDView.as_view(), name='chatmessage-api'),
]