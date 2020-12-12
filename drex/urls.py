"""drex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

# from stream_twitter import views

from django.conf.urls import url, include
from users.views import logout_view, login_process_view, logged_in_home_view, user_register_form_view
from django.contrib.auth.decorators import login_required
from .views import home_view, drex_feature_view, profile, search


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls', namespace='users')),
    path('canvas/', include('canvas.urls', namespace='canvas')),
    path('', home_view, name='home'),
    path('features/', drex_feature_view, name='features'),
    path('profile/', profile, name='profile'),
    path('search/', search, name='search'),
    path('logout/', logout_view, name='logout'),
    path('posts/', include('posts.urls', namespace='posts')),
    path('notifications/', include('actions.urls', namespace='actions')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('api/posts/', include('posts.api.urls', namespace='posts-api')),
    path('api/chat/', include('chat.api.urls', namespace='chat-api')),
    path('course/', include('courses.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)