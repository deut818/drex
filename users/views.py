from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from common.decorators import ajax_required
from django.http import JsonResponse
from .models import User, Contact

from actions.utils import create_action
from actions.models import Action
from webpush import send_user_notification

#Create your views here.
def users_view(request):
    return render(request, "users/login.html", context)

def user_register_form_view(request, *args, **kwargs):
    reg_form = RegistrationForm()
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST or None)
    if reg_form.is_valid():
        reg_form.save()
        # Contact.objects.get_or_create(user_from=request.user, user_to=request.user)
        email = request.POST['email']
        password = request.POST['password2']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/user/welcome')
        # messages.info(request, 'Thanks for registering!')
        # return redirect('/user')

    context = {
        'form': reg_form
    }
    return render(request, "users/reg.html", context)

def login_process_view(request, *args, **kwargs):
    if request.method == 'POST':
        email = request.POST['log_em']
        password = request.POST['log_psw']

        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/profile')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('/user')
    
    return render(request, 'users/login.html',{})

@login_required
def logged_in_home_view(request):
    render(request, 'index.html',{})

def logout_view(request):
    auth.logout(request)
    return render(request, 'users/loggedout.html',{})

class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"

class UserProfileView(DetailView):
    model = User
    template_name = "users/profile/profile.html"
    # def get_context_data(self, ** kwargs):
    #     # context = super().get_context_data( ** kwargs)
    #     # friend = Friend.objects.get(current_user=request.user)
    #     # friends = friend.users.all()
    #     # context['friends'] = friends
    #     # return context

class UserUpdateView(UpdateView):
    model = User
    fields = ['fname', 'lname', 'profile_picture', 'city', 'country', 'email', 'cover_photo', 'username']
    template_name_suffix = '_update_form'
    success_url = '/profile'
    
def user_welcome(request):
    return render(request, "users/welcome.html", {})

@ajax_required
@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
                payload = {"head": "Welcome!", "body": "Hello World"}

                send_user_notification(user=user, payload=payload, ttl=1000)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
                create_action(request.user, 'stopped following', user)
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'ok'})   
    