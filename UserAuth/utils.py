from rest_framework.authentication import SessionAuthentication

class SessionAuth(SessionAuthentication):
    def enforce_csrf(self, request):
        return