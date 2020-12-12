from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, UpdateView, TemplateView, DetailView, DeleteView, CreateView, FormView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse

from common.decorators import ajax_required
from actions.utils import create_action
from .models import Post, Comment
from .forms import PostCreateForm, CommentForm, CommentReplyForm
from webpush import send_user_notification

import redis

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

# Create your views here.
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'posted', new_item)
            messages.success(request, 'Posted Successfuly')
        redirect('profile')
    else:
        form = PostCreateForm()

    return render(request, 'posts/post/create.html', {'section': 'posts', 'form': form})


def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    # increment total image views by 1
    total_views = r.incr('post:{}:views'.format(post.id))
    # increment image ranking by 1
    r.zincrby('post_ranking', post.id, 1)
    return render(request, 'posts/post/detail.html', {'section': 'posts', 'post': post, 'total_views':total_views})


@ajax_required
@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
                create_action(request.user, 'liked', post)
            else:
                post.users_like.remove(request.user)
                create_action(request.user, 'unliked', post)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})

@ajax_required
@login_required
@require_POST
def post_comment(request):
    post_id = request.POST.get('post_id')
    comment = request.POST.get('comm')
    print(post_id, comment)
    if post_id and comment:
        try:
            post = Post.objects.get(id=post_id)
            print(post)
            post.comments.get_or_create(user=request.user, body=comment)
            create_action(request.user, 'commented on', post)
            return JsonResponse({'status': 'ok'})
        except:
            print('Sorry')
    return JsonResponse({'status': 'ok'})

def post_list(request):
    following_ids = request.user.following.values_list('id', flat=True)
    posts_1 = Post.objects.filter(user_id__in=following_ids)
    posts_2 = Post.objects.filter(user_id = request.user.id)
    posts = posts_1.union(posts_2).order_by("-created")
    print(posts)
    user_posts = Post.objects.filter(user_id=request.user.id)
    payload = {"head": "Welcome!", "body": "Hello World", "icon":"https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.tjZtJw237AKsS6BYWPPclAHaFY%26pid%3DApi%26h%3D180%26p%3D0&f=1"}

    send_user_notification(user=request.user, payload=payload, ttl=1000)
    context = {
        'post_list':posts,
        'd_request':request,
        'user_posts':user_posts
    }
    return render(request, "posts/post/list.html", context)

@login_required
def post_ranking(request):# get image ranking dictionary
    post_ranking = r.zrange('post_ranking', 0, -1, desc=True)[:10]
    post_ranking_ids = [int(id) for id in post_ranking]
    # get most viewed images
    most_viewed = list(Post.objects.filter(id__in=post_ranking_ids))
    most_viewed.sort(key=lambda x: post_ranking_ids.index(x.id))
    return render(request, 'posts/post/ranking.html', {'section': 'posts', 'most_viewed': most_viewed})