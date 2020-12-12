from django.urls import path, include

from . import views
app_name= 'actions'

urlpatterns = [
    path('', views.notifications, name='list'),
]