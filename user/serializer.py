from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Представляет сериализатор для модели пользователя.
    Определяет какие поля из модели будут сериализоваться (попадут в JSON-ответ или обработаются при запросе).
    Attributes:
        id (int):           Идентификатор пользователя
        email (str):        Электронная почта пользователя
        first_name (str):   Имя пользователя
        last_name (str):    Фамилия пользователя
    """

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")
