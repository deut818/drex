from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name='posts'
urlpatterns=[
    path('create/', views.post_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', views.post_detail, name='detail'),
    path('like/', views.post_like, name='like'),
    path('comment/', views.post_comment, name='comment'),
    path('', views.post_list, name='list'),
    path('ranking/', views.post_ranking, name='ranking'),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)