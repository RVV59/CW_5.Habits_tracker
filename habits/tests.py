from datetime import timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from habits.models import Habit


class HabitTestCase(APITestCase):
    """Тестовый класс для модели Habit."""

    def setUp(self):
        """
        Настройка начальных данных для тестов.
        Создаем двух пользователей и аутентифицируем первого.
        """
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123')
        self.client.force_authenticate(user=self.user1)

        # Приятная привычка для user1, которую можно будет связать
        self.pleasant_habit = Habit.objects.create(
            user=self.user1,
            action='Выпить стакан воды',
            is_pleasant=True,
            periodicity=1,
            time='08:00:00',
            # ИСПРАВЛЕНО: Преобразуем timedelta в секунды
            duration=int(timedelta(seconds=60).total_seconds()),
            place='Кухня'
        )

        # Обычная привычка для user1
        self.habit1 = Habit.objects.create(
            user=self.user1,
            action='Сделать зарядку',
            periodicity=1,
            time='08:30:00',
            # ИСПРАВЛЕНО: Преобразуем timedelta в секунды
            duration=int(timedelta(seconds=100).total_seconds()),
            place='Комната',
            reward='Съесть яблоко'
        )

        # Привычка для user2, которую user1 не должен видеть/редактировать
        self.habit2 = Habit.objects.create(
            user=self.user2,
            action='Читать книгу',
            periodicity=1,
            time='21:00:00',
            # ИСПРАВЛЕНО: Преобразуем timedelta в секунды
            duration=int(timedelta(seconds=120).total_seconds()),
            place='Спальня',
            reward='Чашка чая'
        )

    def test_habit_create_valid(self):
        """Тест создания валидной привычки."""
        url = reverse('habits:habit-list')
        data = {
            'action': 'Пробежка',
            'place': 'Парк',
            'time': '07:00:00',
            'duration': '00:01:30',  # 90 секунд
            'periodicity': 2,
            'reward': 'Смузи'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 4)
        self.assertTrue(Habit.objects.filter(action='Пробежка').exists())

    def test_habit_create_invalid_duration(self):
        """Тест: нельзя создать привычку с длительностью > 120 секунд."""
        url = reverse('habits:habit-list')
        data = {
            'action': 'Медитация',
            'place': 'Комната',
            'time': '22:00:00',
            'duration': '00:02:01',  # 121 секунда
            'periodicity': 1,
            'reward': 'Спокойный сон'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('duration', response.data)

    def test_habit_create_invalid_reward_and_related(self):
        """Тест: нельзя создать привычку с наградой и связанной привычкой одновременно."""
        url = reverse('habits:habit-list')
        data = {
            'action': 'Планирование дня',
            'place': 'Кабинет',
            'time': '09:00:00',
            'duration': '00:01:00',
            'periodicity': 1,
            'reward': 'Чашка кофе',
            'related_habit': self.pleasant_habit.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_habit_create_invalid_pleasant_habit(self):
        """Тест: у приятной привычки не может быть награды."""
        url = reverse('habits:habit-list')
        data = {
            'action': 'Слушать музыку',
            'place': 'Везде',
            'time': '18:00:00',
            'duration': '00:01:00',
            'periodicity': 1,
            'is_pleasant': True,
            'reward': 'Хорошее настроение'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_habit_list(self):
        """Тест получения списка привычек (только своих)."""
        url = reverse('habits:habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем пагинацию и что user1 видит только свои 2 привычки
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['action'], self.pleasant_habit.action)

    def test_habit_update_own(self):
        """Тест обновления своей привычки."""
        url = reverse('habits:habit-detail', args=[self.habit1.id])
        data = {'reward': 'Посмотреть серию сериала'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit1.refresh_from_db()
        self.assertEqual(self.habit1.reward, 'Посмотреть серию сериала')

    def test_habit_update_foreign(self):
        """Тест: нельзя обновить чужую привычку."""
        url = reverse('habits:habit-detail', args=[self.habit2.id])
        data = {'reward': 'Попытка взлома'}
        response = self.client.patch(url, data, format='json')
        # DRF вернет 404, так как по правилам IsOwner чужой объект не найден
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_habit_delete_foreign(self):
        """Тест: нельзя удалить чужую привычку."""
        url = reverse('habits:habit-detail', args=[self.habit2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Habit.objects.filter(id=self.habit2.id).exists())

    def test_habit_delete_own(self):
        """Тест успешного удаления своей привычки."""
        url = reverse('habits:habit-detail', args=[self.habit1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.habit1.id).exists())
