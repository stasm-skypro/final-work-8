from django.db import models


class Habit(models.Model):
    """
    Представляет модель привычки.
    Attributes:
        user (User):                Пользователь — создатель привычки
        place (str):                Место выполнения привычки
        time (time):                Время выполнения привычки
        action (str):               Действие, которое представляет собой привычку
        is_pleasant (bool):         Признак приятной привычки
        related_habit (Habit):      Связанная привычка
        periodicity (int):          Периодичность выполнения привычки
        reward (str):               Вознаграждение
        duration (duration):        Время на выполнение
        is_public (bool):           Признак публичности привычки
        created_at (datetime):      Дата и время создания привычки
    """

    # Пользователь — создатель привычки
    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",  # определяет имя обратной связи — то, как обращаться к связанным объектам с
        # другой стороны связи
    )

    # Место — место, в котором необходимо выполнять привычку
    place = models.CharField(max_length=255, verbose_name="Место")

    # Время — время, когда необходимо выполнять привычку
    time = models.TimeField(verbose_name="Время")

    # Действие — действие, которое представляет собой привычка
    action = models.CharField(max_length=255, verbose_name="Действие")

    # Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")

    # Связанная привычка — привычка, которая связана с другой привычкой, важно указывать для полезных привычек, но не
    # для приятных
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Указывается только для полезных привычек",
    )

    # Периодичность (по умолчанию ежедневная) — периодичность выполнения привычки для напоминания в днях
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name="Периодичность (в днях)")

    # Вознаграждение — чем пользователь должен себя вознаградить после выполнения
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вознаграждение")

    # Время на выполнение — время, которое предположительно потратит пользователь на выполнение привычки
    duration = models.DurationField(verbose_name="Время на выполнение")

    # Признак публичности — привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример
    # чужие привычки
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    # Дата создания привычки
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")

    def __str__(self) -> str:
        """
        Возвращает строковое представление привычки
        :return: Строковое представление привычки
        """
        return f"{self.action} - ({self.user})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
