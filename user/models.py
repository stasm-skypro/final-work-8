from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """
    Определяет менеджера пользователей. Нужен для правильного создания пользователей и суперпользователей в кастомной
    модели пользователя.
    Attributes:
        email (str):        Электронная почта пользователя
        password (str):     Пароль пользователя
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создаёт обычного пользователя.
        :param email:           Электронная почта пользователя
        :param password:        Пароль пользователя
        :param extra_fields:    Дополнительные поля пользователя
        :return:                Объект пользователя
        """
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создаёт суперпользователя.
        :param email:           Электронная почта суперпользователя
        :param password:        Пароль суперпользователя
        :param extra_fields:    Дополнительные поля суперпользователя
        :return:                Объект суперпользователя
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Проверка, чтобы избежать ситуаций, когда суперпользователь создаётся без нужных прав
        if not extra_fields["is_staff"]:
            raise ValueError("У суперпользователя должно быть is_staff=True.")
        if not extra_fields["is_superuser"]:
            raise ValueError("У суперпользователя должно быть is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Определяет модель пользователя.
    Attributes:
        email (str):            Электронная почта пользователя
        first_name (str):       Имя пользователя
        last_name (str):        Фамилия пользователя
        is_active (bool):       Признак, является ли пользователь активным
        is_staff (bool):        Признак, является ли пользователь суперпользователем
        is_superuser (bool):    Признак, является ли пользователь суперпользователем
        date_joined (datetime): Дата и время регистрации
    """

    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=30, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=30, blank=True, verbose_name="Фамилия")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Сотрудник")
    is_superuser = models.BooleanField(default=False, verbose_name="Суперпользователь")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []  # поля, требуемые при создании суперпользователя (кроме email и пароля)
    # нам никаких не нужно

    def __str__(self):
        """
        Возвращает строковое представление пользователя.
        :return: Строковое представление пользователя
        """
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
