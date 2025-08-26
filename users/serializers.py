from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра и редактирования профиля пользователя.
    Не включает и не принимает пароль.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city', 'avatar')


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового пользователя (регистрации).
    Принимает email и password, но не возвращает пароль в ответе.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Этот метод переопределяется, чтобы использовать create_user.
        Это гарантирует, что пароль будет правильно хеширован.
        """
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
