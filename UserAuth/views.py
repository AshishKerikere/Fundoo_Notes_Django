from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login

# from rest_framework import viewsets
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView
from rest_framework.views import APIView

from .serializers import RegistrationSerializer, LoginSerializer
from UserAuth.utils import SessionAuth
from .models import User

from rest_framework_simplejwt.authentication import JWTAuthentication
"""def FundooViews(request):

    return HttpResponse('FundooNotes Under Development')"""


class RegistrationAPI(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "UserRegistered", "status": 200, "data": serializer.data}, status=200)


"""class LoginAPI(LoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer
    authentication_classes = [SessionAuth]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)"""


# Create your views here.

class UserLoginAPI(APIView):
    serializer_class = LoginSerializer
    #serializer_class = AuthTokenSerializer
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "Login Successful", "status": 200, "data": {}}, status=200)

# Create your views here.
