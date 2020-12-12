from django.urls import path, include

from . import views

app_name = 'canvas'
urlpatterns = [
    path('', views.IndexPage, name="index"),
]