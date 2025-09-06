# C:/Users/Vlad/PycharmProjects/CW_5.Habits_tracker/users/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    """Тест-кейс для модели User."""

    def setUp(self):
        """Подготовка данных для тестов."""
        self.user = User.objects.create(
            email='test@example.com',
            is_staff=False,
            is_superuser=False,
            is_active=True
        )
        self.user.set_password('testpassword')
        self.user.save()

    def test_user_registration(self):
        """Тестирование создания (регистрации) пользователя."""
        # ИСПРАВЛЕНО: Используем имя 'user-list' для POST-запроса на создание
        url = reverse('users:user-list')
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123"
        }

        response = self.client.post(url, data, format='json')

        # 1. Проверяем, что пользователь успешно создан (статус 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2. Проверяем, что в базе данных теперь два пользователя
        self.assertEqual(User.objects.count(), 2)

        # 3. Проверяем, что email нового пользователя соответствует отправленному
        self.assertEqual(response.data['email'], data['email'])

        # 4. Убеждаемся, что пароль не возвращается в ответе
        self.assertNotIn('password', response.data)

    def test_user_login(self):
        """Тестирование аутентификации пользователя и получения JWT токена."""
        # ИСПРАВЛЕНО: Указываем namespace 'users' для токена
        url = reverse('users:token_obtain_pair')
        data = {
            "email": self.user.email,
            "password": "testpassword"
        }

        response = self.client.post(url, data, format='json')

        # 1. Проверяем, что аутентификация прошла успешно (статус 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2. Проверяем, что в ответе есть access и refresh токены
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_profile_permissions(self):
        """Тестирование прав доступа к профилям."""
        # Создаем второго пользователя
        other_user = User.objects.create(email='other@example.com')
        other_user.set_password('otherpass')
        other_user.save()

        # Аутентифицируемся как первый пользователь
        self.client.force_authenticate(user=self.user)

        # 1. Пытаемся получить доступ к своему профилю (должно быть разрешено)
        my_profile_url = reverse('users:user-detail', args=[self.user.pk])
        my_response = self.client.get(my_profile_url)
        self.assertEqual(my_response.status_code, status.HTTP_200_OK)

        # 2. Пытаемся получить доступ к чужому профилю (должно быть запрещено)
        other_profile_url = reverse('users:user-detail', args=[other_user.pk])
        other_response = self.client.get(other_profile_url)

        # ИСПРАВЛЕНО: Теперь ожидаем 403 Forbidden, так как IsOwner будет работать корректно
        self.assertEqual(other_response.status_code, status.HTTP_403_FORBIDDEN)
