# habits/permissions.py

from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Кастомное правило доступа.
    Разрешает доступ только владельцу объекта.
    """
    message = "Вы не являетесь владельцем этой привычки."

    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ, если пользователь, делающий запрос,
        # является тем же, кто указан в поле 'user' объекта.
        return obj.user == request.user