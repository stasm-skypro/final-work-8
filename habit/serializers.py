from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def validate_reward_or_related(self, attrs):
        """
        Исключает одновременное указание вознаграждения и связанной привычки.
        :param attrs:
        :return:
        """
        related = attrs.get("related_habit")
        reward = attrs.get("reward")

        if related and reward:
            raise serializers.ValidationError("Укажите либо вознаграждение, либо связанную привычку, но не оба поля.")

        if attrs.get("is_pleasant") and (related or reward):
            raise serializers.ValidationError(
                "У приятной привычки не может быть награды или связи с другой привычкой."
            )

        return attrs

    def validate_time_to_complete(self, value):
        """
        Исключает выполнение привычки более 120 секунд.
        """
        if value > 120:
            raise ValidationError("Время выполнения не может превышать 120 секунд.")
        return value

    def validate_related_habit(self, value):
        """
        Проверяет, что в связанные привычки могут попадать только привычки с признаком приятной привычки.
        """
        if value and not value.is_pleasant:
            raise ValidationError("Связанная привычка должна быть с признаком приятной привычки.")
        return value

    def validate_pleasant_restrictions(self, value):
        """
        Исключает появление у приятной привычки вознаграждение или связанной привычки.
        """
        if value.is_pleasant and (value.reward or value.related_habit):
            raise ValidationError("У приятной привычки не должно быть ни вознаграждения, ни связанной привычки.")
        return value

    def validate_frequency(self, value):
        """
        Проверяет периодичность выполнения привычки. Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
        """
        if value > 7:
            raise ValidationError("Периодичность не может быть больше 7 дней.")
        return value
