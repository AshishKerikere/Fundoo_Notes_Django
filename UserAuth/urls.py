from .views import RegistrationAPI, UserLoginAPI
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('api/registeruser/', RegistrationAPI.as_view(), name='register'),
    #path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/loginuser/', UserLoginAPI.as_view(), name='login'),
]