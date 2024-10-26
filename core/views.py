from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegisterSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserLoginView(APIView):
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль')
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Успешный вход",
                examples={"application/json": {"refresh": "string", "access": "string"}}
            ),
            401: openapi.Response(description="Неверные учетные данные")
        }
    )
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Аутентификация пользователя
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    

class UserRegisterView(APIView):
    
    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            201: openapi.Response(
                description="Регистрация прошла успешно",
                examples={"application/json": {"message": "User registered successfully!", "refresh": "string", "access": "string"}}
            ),
            400: "Ошибка валидации данных"
        }
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Создаем нового пользователя
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
