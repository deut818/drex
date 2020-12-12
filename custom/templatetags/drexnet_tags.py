from django import template
from django.conf import settings
from posts.forms import PostCreateForm, CommentForm, CommentReplyForm
from posts.models import Post
from actions.utils import create_action
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

register = template.Library()
import redis

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


@register.filter(name='cashuer')
def cashuer(value):
    number = int(value)
    num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if number >= 1000 and number < 10000:
        first = int(str(number)[0])
        second = int(str(number)[1])
        value = f'{first}.{second}k'
    elif number >= 10000 and number < 100000:
        first = int(str(number)[0])
        second = int(str(number)[1])
        third = int(str(number)[2])
        value = f'{first}{second}.{third}k'
    elif number >= 100000 and number < 1000000:
        first = int(str(number)[0])
        second = int(str(number)[1])
        third = int(str(number)[2])
        forth = int(str(number)[3])
        value = f'{first}{second}{third}.{forth}k'
    elif number >= 1000000 and number < 10000000:
        first = int(str(number)[0])
        second = int(str(number)[1])
        value = f'{first}.{second}M'
    elif number >= 10000000 and number < 100000000:
        first = int(str(number)[0])
        second = int(str(number)[1])
        third = int(str(number)[2])
        value = f'{first}{second}.{third}M'
    elif number >= 100000000 and number < 1000000000:
        first = int(str(number)[0])
        second = int(str(number)[1])
        third = int(str(number)[2])
        forth = int(str(number)[3])
        value = f'{first}{second}{third}.{forth}M'
    else:
        pass
    return value

@register.filter(name="viewscount")
def viewscount(value):
    post = value
    # increment total image views by 1
    total_views = r.incr('post:{}:views'.format(post.id))
    # increment image ranking by 1
    r.zincrby('post_ranking', post.id, 1)
    return total_views



@register.inclusion_tag("posts/post/create.html", takes_context=True)
def createpost(context):
    d_request = context['d_request']
    form = PostCreateForm(d_request.POST, d_request.FILES)
    if d_request.method == 'POST':
        if form.is_valid():
            form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = d_request.user
            new_item.save()
            create_action(d_request.user, 'posted', new_item)
            messages.success(d_request, 'Posted Successfuly')

            return redirect('posts:list')
    else:
        form = PostCreateForm()
    return {
        'form':form
    }