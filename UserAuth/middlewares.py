from datetime import datetime
from .models import UserLog

class UserLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def logtracker(self, method, url, user):
        try:
            user_log = UserLog.objects.get(method=method, url=url, user=user)
            user_log.count += 1
            user_log.updated_at = datetime.now()
            user_log.save()
        except UserLog.DoesNotExist:
            UserLog.objects.create(method=method, url=url, user=user)

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            self.logtracker(request.method, request.path, request.user)
        return response
