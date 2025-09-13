from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Конфигурация админ-панели для модели Habit.
    """
    list_display = ('user', 'action', 'place', 'time', 'is_pleasant', 'periodicity', 'reward')
    list_filter = ('user', 'is_pleasant', 'periodicity')
    search_fields = ('action', 'place', 'user__email')

    def get_queryset(self, request):
        """
        Переопределяем queryset, чтобы администраторы видели все привычки,
        а обычные пользователи — только свои.
        """
        # Получаем базовый queryset (все объекты Habit)
        qs = super().get_queryset(request)

        # Если текущий пользователь — суперпользователь, он видит всё.
        if request.user.is_superuser:
            return qs

        # Иначе, пользователь видит только свои привычки.
        return qs.filter(user=request.user)
