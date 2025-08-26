from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели привычки."""

    class Meta:
        model = Habit
        fields = (
            'id', 'place', 'time', 'action', 'is_pleasant',
            'related_habit', 'periodicity', 'reward', 'duration', 'is_public'
        )

    def validate(self, data):
        """
        Добавляем валидацию бизнес-логики прямо в сериализатор.
        Этот метод вызывается перед созданием или обновлением объекта.
        """
        related_habit = data.get('related_habit', getattr(self.instance, 'related_habit', None))
        reward = data.get('reward', getattr(self.instance, 'reward', None))
        is_pleasant = data.get('is_pleasant', getattr(self.instance, 'is_pleasant', None))
        duration = data.get('duration', getattr(self.instance, 'duration', None))
        periodicity = data.get('periodicity', getattr(self.instance, 'periodicity', None))

        if related_habit and reward:
            raise serializers.ValidationError('Нельзя одновременно указывать связанную привычку и вознаграждение.')

        if duration and duration > 120:
            raise serializers.ValidationError('Время выполнения не может превышать 120 секунд.')

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError('В связанные привычки могут попадать только привычки с признаком "приятной".')

        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')

        if periodicity and periodicity > 7:
            raise serializers.ValidationError('Периодичность не может быть реже, чем раз в 7 дней.')

        return data