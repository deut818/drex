from django.shortcuts import render

from .models import Action
# Create your views here.
def notifications(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user').prefetch_related('target')[:10]
    else:
        pass

    context = {
        'actions':actions
    }
    return render(request, "actions/action/list.html", context)