from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required

from users.models import User

def home_view(request, *args, **kwargs):
    context = {
        'welcome': 'WELCOME TO DREXNET'
    }
    return render(request, "index.html", context)
    
@login_required
def drex_feature_view(request, *args, **kwargs):
    context = {}
    return render(request, 'features.html',context)

@login_required
def profile(request):
    user_obj = request.user.date_of_birth
    current_year = timezone.now().year
    age = current_year - user_obj.year
    context = {
        "user_age":age,
    }
    return render(request, 'profile/profile.html', context)

def search(request):
    queryset = User.objects.all()
    query = request.GET.get("q")
    if query:
        queryset = queryset.filter(
            Q(fname__icontains=query) |
            Q(lname__icontains=query)
        ).distinct()
        message = f"Results found for <i>'{query}'</i>"
    context = {
        'query_set':queryset,
        'message':message
    }
    return render(request, 'base/search_results.html', context)


