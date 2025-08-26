import random
from django.core.management.base import BaseCommand
from faker import Faker
from users.models import User
from habits.models import Habit

# Создаем экземпляр Faker для генерации данных
fake = Faker('ru_RU')


class Command(BaseCommand):
    """
    Кастомная Django-команда для заполнения базы данных тестовыми данными.
    """
    help = 'Заполняет базу данных тестовыми пользователями и привычками'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начинаем очистку старых данных...")
        # Очищаем старые данные, чтобы избежать дубликатов
        Habit.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()  # Удаляем всех, кроме админов
        self.stdout.write(self.style.SUCCESS("Старые данные успешно удалены."))

        self.stdout.write("Создаем новых пользователей...")
        users = []
        for _ in range(10):  # Создадим 10 пользователей
            user = User.objects.create_user(
                email=fake.email(),
                password='password123',  # Простой пароль для всех тестовых юзеров
                phone=fake.phone_number(),
                city=fake.city()
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"Создано {len(users)} пользователей."))

        self.stdout.write("Создаем привычки...")
        pleasant_habits = []
        useful_habits = []

        # Сначала создаем "приятные" привычки, на которые можно будет ссылаться
        for user in users:
            for _ in range(random.randint(1, 2)):  # 1-2 приятные привычки на пользователя
                habit = Habit.objects.create(
                    user=user,
                    place=fake.street_name(),
                    time=fake.time(),
                    action=f"Выпить {random.choice(['кофе', 'чай', 'стакан воды'])}",
                    is_pleasant=True,
                    periodicity=random.randint(1, 3),
                    duration=random.randint(30, 60),
                    is_public=random.choice([True, False])
                )
                pleasant_habits.append(habit)

        # Теперь создаем "полезные" привычки
        for user in users:
            for _ in range(random.randint(2, 4)):  # 2-4 полезные привычки на пользователя
                # Решаем, будет ли у привычки вознаграждение или связанная привычка
                has_reward = random.choice([True, False])

                related_habit = None
                reward = None

                if not has_reward and pleasant_habits:
                    # Выбираем случайную приятную привычку (не обязательно свою)
                    related_habit = random.choice(pleasant_habits)
                else:
                    reward = f"Посмотреть серию {random.choice(['сериала', 'аниме', 'фильма'])}"

                habit = Habit.objects.create(
                    user=user,
                    place=random.choice(['Дом', 'Офис', 'Спортзал']),
                    time=fake.time(),
                    action=f"Сделать {random.choice(['зарядку', 'планку', 'пробежку'])}",
                    is_pleasant=False,
                    related_habit=related_habit,
                    reward=reward,
                    periodicity=random.randint(1, 7),  # Периодичность до 7 дней
                    duration=random.randint(60, 120),  # Длительность до 120 секунд
                    is_public=random.choice([True, False])
                )
                useful_habits.append(habit)

        self.stdout.write(self.style.SUCCESS(f"Создано {len(pleasant_habits)} приятных привычек."))
        self.stdout.write(self.style.SUCCESS(f"Создано {len(useful_habits)} полезных привычек."))
        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))
