from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Habit
from .serializers import HabitSerializer


class UserHabitListAPIView(APIView):
    """
    Возвращает список привычек текущего пользователя с пагинацией.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Обрабатывает GET-запрос и возвращает список привычек текущего пользователя с пагинацией.
        :param request: rest_framework.request.Request
        :return: Response
        """
        habits = Habit.objects.filter(user=request.user).order_by("created_at")
        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(habits, request)
        serializer = HabitSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
