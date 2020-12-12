from django.core.cache import cache
from django.conf import settings
import datetime

class ActiveUserMiddleware:
    def process_request(request, self):
        current_user = request.user
        if request.user.is_authenticated():
            now = datetime.datetime.now()
            cache.set('seen_%s' (current_user.username), now, settings.USER_LASTSEEN_TIMEOUT)