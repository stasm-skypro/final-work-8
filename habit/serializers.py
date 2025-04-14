"""
Модуль сериализатора модели Habit.
RewardOrRelatedValidator и PleasantRestrictionsValidator — используются в Meta.validators так как они работают
с несколькими полями одновременно.
MaxDurationValidator, FrequencyValidator, RelatedHabitValidator — подключены к конкретным полям через validators=[...].
Типы полей:
DurationField валидируется через value.total_seconds().
'related_habit' задан как PrimaryKeyRelatedField, при этом валидатор принимает саму модель.
"""

from rest_framework import serializers

from .models import Habit, PleasantHabit
from .validators import (
    FrequencyValidator,
    MaxDurationValidator,
    PleasantRestrictionsValidator,
    RelatedHabitValidator,
    RewardOrRelatedValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    """
    Проверяет валидность привычки согласно бизнес-правилам.
    """

    duration = serializers.DurationField(validators=[MaxDurationValidator()], required=True)
    related_habit = serializers.PrimaryKeyRelatedField(
        queryset=PleasantHabit.objects.all(),
        required=False,
        allow_null=True,
        validators=[RelatedHabitValidator()],
    )
    periodicity = serializers.IntegerField(validators=[FrequencyValidator()])

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RewardOrRelatedValidator(),
            PleasantRestrictionsValidator(),
        ]


# class HabitSerializer(serializers.ModelSerializer):
#     """
#     Подготавливает список привычек.
#     """
#
#     class Meta:
#         model = Habit
#         fields = "__all__"
