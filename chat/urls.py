from django.urls import path, re_path


from .views import ThreadView, InboxView

app_name = 'chat'
urlpatterns = [
    path("", InboxView.as_view(), name='inbox'),
    re_path(r"^messages/(?P<username>[\w.@+-]+)/$", ThreadView.as_view(), name='chat_room'),
]
