from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .serializers import UserRegistrationSerializer
import logging
logger = logging.getLogger(__name__)


# Create your views here.
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info("User get accessed by: %s \n", request.user)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info("User %s created", user.username)
            return Response({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
