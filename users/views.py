from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer, UserCreateSerializer
from .permissions import IsOwner


class UserCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для регистрации нового пользователя.
    """
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserListAPIView(generics.ListAPIView):
    """
    Эндпоинт для просмотра списка пользователей.
    Доступен только авторизованным пользователям.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Эндпоинт для просмотра, обновления и удаления ОДНОГО пользователя.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
