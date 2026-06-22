from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer



class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]