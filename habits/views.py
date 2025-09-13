from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwner
from rest_framework.permissions import AllowAny


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с привычками.
    """
    serializer_class = HabitSerializer
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


class PublicHabitListAPIView(generics.ListAPIView):
    """
    Контроллер для просмотра списка публичных привычек.
    Доступен всем пользователям (даже неавторизованным).
    """
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Возвращает только те привычки, у которых установлен флаг is_public=True.
        """
        return Habit.objects.filter(is_public=True)
