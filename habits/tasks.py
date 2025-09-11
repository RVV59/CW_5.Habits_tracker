from celery import shared_task
import requests
from datetime import datetime
from django.conf import settings
from .models import Habit


@shared_task
def send_telegram_notification(habit_id):
    """
    Задача для отправки уведомления в Telegram о выполнении привычки.
    """
    try:
        habit = Habit.objects.get(id=habit_id)
        user = habit.user
        if user.chat_id:
            message = (f"Напоминание! Сегодня в {habit.time.strftime('%H:%M')} вам нужно выполнить привычку:"
                       f" {habit.action}. Место: {habit.place}.")
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            params = {
                "chat_id": user.chat_id,
                "text": message,
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            print(f"Уведомление для привычки {habit.id} успешно отправлено пользователю {user.email}.")
        else:
            print(f"У пользователя {user.email} не указан chat_id.")
    except Habit.DoesNotExist:
        print(f"Привычка с id={habit_id} не найдена.")
    except requests.RequestException as e:
        print(f"Ошибка отправки уведомления для привычки {habit_id}: {e}")


@shared_task
def schedule_habit_notifications():
    """
    Периодическая задача, которая проверяет все привычки
    и ставит в очередь отправку уведомлений для тех, у кого подошло время.
    """
    print("Запуск периодической задачи schedule_habit_notifications...")
    now = datetime.now().time()

    habits_to_notify = Habit.objects.filter(
        time__hour=now.hour,
        time__minute=now.minute,
        is_pleasant=False
    )

    for habit in habits_to_notify:
        # Проверяем периодичность
        # timedelta(days=1) - для ежедневных, timedelta(days=7) - для еженедельных
        # Здесь для простоты будем считать, что все привычки ежедневные
        # В реальном проекте логика была бы сложнее, с учетом поля 'periodicity'
        print(f"Найдена привычка для уведомления: {habit.id}")
        send_telegram_notification.delay(habit.id)
