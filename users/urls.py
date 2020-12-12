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
from django.conf.urls import url, include
from django.urls import path
from users.views import user_register_form_view, login_process_view, logged_in_home_view, logout_view, UserListView, UserProfileView, UserUpdateView, user_welcome, user_follow
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


app_name = 'users'
urlpatterns = [
    path('login/', login_process_view, name='login'),
    path('signup/', user_register_form_view, name='signup'),
    path('home/', logged_in_home_view, name='user_logged_in'),
    path('logout/', logout_view, name='logout'),
    path('welcome/', user_welcome, name='user_welcome'),
    path('list/', login_required(UserListView.as_view()), name='users_list'),
    path('update/<int:pk>/', login_required(UserUpdateView.as_view()), name='user_update'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='user-profile'),
    path('follow/', user_follow, name='user_follow'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name="users/password_change_form.html", success_url="/change-password/done"),name='password_change'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),name='password_change_done'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name="users/password_reset_form.html", email_template_name="users/password_reset_email.html", subject_template_name="users/password_reset_subject.txt", success_url="/user/reset-password/done"), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html", success_url="/user/reset/done"),name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),name='password_reset_complete'),
    # path()
]
