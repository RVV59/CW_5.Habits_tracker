
from datetime import timedelta
from rest_framework import serializers
from habits.models import Habit
from habits.validators import (
    validate_reward_and_related_habit,
    validate_duration,
    validate_related_habit_is_pleasant,
    validate_pleasant_habit_has_no_reward_or_related,
    validate_periodicity
)

class IntegerDurationField(serializers.DurationField):
    """
    Кастомное поле, которое корректно работает в обе стороны:
    - Принимает строку "HH:MM:SS" и сохраняет в БД как Integer (секунды).
    - Читает Integer из БД и отдает в JSON как строку "HH:MM:SS".
    """
    def to_representation(self, value):
        duration_timedelta = timedelta(seconds=value)
        return super().to_representation(duration_timedelta)

    def to_internal_value(self, value):
        duration_timedelta = super().to_internal_value(value)
        return int(duration_timedelta.total_seconds())

class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit."""

    duration = IntegerDurationField(validators=[validate_duration])

    user = serializers.SlugRelatedField(
        slug_field='email',
        read_only=True
    )

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            validate_reward_and_related_habit,
            validate_related_habit_is_pleasant,
            validate_pleasant_habit_has_no_reward_or_related,
            validate_periodicity,
        ]
