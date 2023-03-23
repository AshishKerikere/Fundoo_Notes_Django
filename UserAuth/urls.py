from .views import RegistrationAPI, UserLoginAPI
from django.urls import path

urlpatterns = [
    path('api/registeruser/', RegistrationAPI.as_view(), name='register'),
    path('api/loginuser/', UserLoginAPI.as_view(), name='login'),
]