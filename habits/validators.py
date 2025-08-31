from rest_framework.exceptions import ValidationError
from datetime import timedelta

def validate_reward_and_related_habit(value):
    """
    Проверяет, что одновременно не выбраны и награда, и связанная привычка.
    """
    related_habit = value.get('related_habit')
    reward = value.get('reward')

    if related_habit and reward:
        raise ValidationError("Нельзя одновременно указывать связанную привычку и вознаграждение.")

def validate_duration(value):
    """
    Проверяет, что время выполнения не превышает 120 секунд.
    """
    if value > 120:
        raise ValidationError("Время выполнения привычки не может превышать 120 секунд.")

def validate_related_habit_is_pleasant(value):
    """
    Проверяет, что в связанные привычки могут попадать только привычки с признаком приятной.
    """
    related_habit = value.get('related_habit')
    if related_habit and not related_habit.is_pleasant:
        raise ValidationError("В связанные привычки могут попадать только привычки с признаком 'приятной'.")

def validate_pleasant_habit_has_no_reward_or_related(value):
    """
    Проверяет, что у приятной привычки не может быть вознаграждения или связанной привычки.
    """
    is_pleasant = value.get('is_pleasant')
    reward = value.get('reward')
    related_habit = value.get('related_habit')

    if is_pleasant and (reward or related_habit):
        raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

def validate_periodicity(value):
    """
    Проверяет, что привычку нельзя выполнять реже, чем 1 раз в 7 дней.
    """
    periodicity = value.get('periodicity')
    if periodicity and periodicity > 7:
        raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")
