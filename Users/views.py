from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# User Registration (Open to anyone)
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Anyone can register

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "User registered successfully",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login (Open to anyone)
class LoginView(APIView):
    permission_classes = [AllowAny]  # Anyone can log in

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            response = {
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            }
            return Response(data=response, status=status.HTTP_200_OK)
        
        return Response(data={"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Protected Route: Get Current User (Requires Authentication)
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can access

    def get(self, request, *args, **kwargs):
        user = request.user  # Authenticated user
        response = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return Response(data=response, status=status.HTTP_200_OK)
