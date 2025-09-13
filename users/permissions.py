from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Права доступа, которые позволяют редактировать объект только его владельцу.
    """
    def has_object_permission(self, request, view, obj):
        # Если модель - это сам User, сравниваем напрямую
        if isinstance(obj, request.user.__class__):
            return obj == request.user
        # Для остальных моделей (например, Habit) ищем поле 'user'
        return obj.user == request.use
