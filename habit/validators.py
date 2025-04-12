from rest_framework.exceptions import ValidationError

# def validate_reward_or_related(data):
#     """
#     Исключает одновременное указание вознаграждения и связанной привычки.
#     """
#     if data.get("reward") and data.get("related_habit"):
#         raise ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")


class ValidateRewardOrRelated:
    """
    Исключает одновременное указание вознаграждения и связанной привычки.
    """

    def __init__(self, field):
        """
        :param field:
        """
        self.field = field

    def __call__(self, value):

        if value.get("reward") and value.get("related_habit"):
            raise ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")


def validate_time_to_complete(value):
    """
    Исключает выполнение привычки более 120 секунд.
    """
    if value > 120:
        raise ValidationError("Время выполнения не может превышать 120 секунд.")


def validate_related_habit(value):
    """
    Проверяет, что в связанные привычки могут попадать только привычки с признаком приятной привычки.
    """
    if value and not value.is_pleasant:
        raise ValidationError("Связанная привычка должна быть с признаком приятной привычки.")


def validate_pleasant_restrictions(value):
    """
    Исключает появление у приятной привычки вознаграждение или связанной привычки.
    """
    if value.is_pleasant and (value.reward or value.related_habit):
        raise ValidationError("У приятной привычки не должно быть ни вознаграждения, ни связанной привычки.")


def validate_frequency(value):
    """
    Проверяет периодичность выполнения привычки. Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
    """
    if value > 7:
        raise ValidationError("Периодичность не может быть больше 7 дней.")
