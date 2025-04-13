from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializer import RegisterSerializer


class RegisterAPIView(APIView):
    """
    Регистрация нового пользователя.

    Параметры запроса:
    - email (str): Email пользователя
    - password (str): Пароль не менее 8 символов
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Обрабатывает запрос на регистрацию нового пользователя.
        :param request: Объект запроса, содержащий данные пользователя.
                    Тип: rest_framework.request.Request
        :return: Response с результатом регистрации.
        """
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": f"Регистрация пользователя {user.email} прошла успешно."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    Аутентификация (авторизация) пользователя.

    Параметры запроса:
    - email (str): Email пользователя
    - password (str): Пароль

    Ответ:
    - access: JWT токен доступа
    - refresh: JWT токен обновления
    """

    def post(self, request):
        """
        Обрабатывает запрос на аутентификацию пользователя.
        :param request: Объект запроса, содержащий данные пользователя.
                    Тип: rest_framework.request.Request
        :return: Response с результатом аутентификации.
        """
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({"access": str(refresh.access_token), "refresh": str(refresh)})
        return Response({"detail": "Неверный email или пароль."}, status=status.HTTP_401_UNAUTHORIZED)
