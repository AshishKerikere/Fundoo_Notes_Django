
from rest_framework.response import Response

from rest_framework.views import APIView

from .serializers import RegistrationSerializer, LoginSerializer

class RegistrationAPI(APIView):
    serializer_class = RegistrationSerializer
    authentication_classes = []
    permission_classes = []
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "UserRegistered", "status": 200, "data": serializer.data}, status=200)

# Create your views here.

class UserLoginAPI(APIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        # def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "Login Successful", "status": 200, "data": {}}, status=200)

# Create your views here.
