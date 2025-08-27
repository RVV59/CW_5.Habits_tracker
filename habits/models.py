from django.db import models
from django.conf import settings
# Словарь для полей, которые могут быть пустыми в базе данных и в формах.
# Удобно, чтобы не дублировать код. Близнецы научили.
NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    """Модель привычки."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Создатель привычки'
    )
    place = models.CharField(max_length=200, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=200, verbose_name='Действие')
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )

    # Связанная привычка (может быть, а может и не быть)
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name='Связанная привычка'
    )

    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Периодичность в днях'
    )
    reward = models.CharField(
        max_length=200,
        **NULLABLE,
        verbose_name='Вознаграждение'
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name='Время на выполнение в секундах'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('pk',)
