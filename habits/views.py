# habits/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated # <-- Важно для безопасности

from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwner # <-- Предполагаем, что у вас будет такой permission

class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с привычками.
    """
    serializer_class = HabitSerializer
    # Указываем права доступа: пользователь должен быть авторизован,
    # а для редактирования/удаления - быть владельцем.
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        Этот метод определяет, какой список объектов вернется пользователю.
        Мы возвращаем только привычки, принадлежащие текущему пользователю.
        """
        user = self.request.user
        return Habit.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Этот метод вызывается при создании нового объекта.
        Мы автоматически привязываем новую привычку к текущему пользователю.
        """
        serializer.save(user=self.request.user)

