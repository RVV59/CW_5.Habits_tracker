from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Кастомное правило доступа.
    Разрешает полный доступ владельцу объекта.
    Разрешает безопасные методы (GET, HEAD, OPTIONS) всем остальным.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS запросы всем
        if request.method in SAFE_METHODS:
            return True

        # Разрешаем запись (PUT, PATCH, DELETE) только владельцу объекта
        return obj == request.user
