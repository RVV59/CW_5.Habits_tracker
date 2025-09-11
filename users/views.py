# C:/Users/Vlad/PycharmProjects/CW_5.Habits_tracker/users/views.py

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import User
from .permissions import IsOwner
from .serializers import UserSerializer, UserCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с пользователями.
    - Создание (регистрация) доступно всем.
    - Список доступен только администраторам.
    - Просмотр/изменение/удаление доступно только владельцу профиля.
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Возвращает разный сериализатор в зависимости от действия.
        Для 'create' используется UserCreateSerializer (с записью пароля),
        для остальных - UserSerializer (без полей пароля).
        """
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        """
        Возвращает разные права доступа в зависимости от действия.
        """
        if self.action == 'create':
            # Разрешаем любому пользователю создавать аккаунт
            self.permission_classes = [AllowAny]
        elif self.action == 'list':
            # Список пользователей могут просматривать только администраторы
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            # Управлять своим профилем может только его владелец
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()
