# from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

# from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Habit
from .serializers import HabitSerializer

# TODO: Переписать через ViewSet
# class UserHabitListAPIView(APIView):
#     """
#     Возвращает список привычек текущего пользователя с пагинацией.
#     """
#
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         """
#         Обрабатывает GET-запрос и возвращает список привычек текущего пользователя с пагинацией.
#         :param request: rest_framework.request.Request
#         :return: Response
#         """
#         habits = Habit.objects.filter(user=request.user).order_by("created_at")
#         paginator = PageNumberPagination()
#         paginated_queryset = paginator.paginate_queryset(habits, request)
#         serializer = HabitSerializer(paginated_queryset, many=True)
#         return paginator.get_paginated_response(serializer.data)


class HabitViewSet(ModelViewSet):
    """
    CRUD для привычек текущего пользователя.

    Эндпойнты:
    GET /habits/ — список привычек текущего пользователя (с пагинацией),
    POST /habits/ — создание,
    GET /habits/{id}/ — просмотр,
    PUT /habits/{id}/ — полное обновление,
    PATCH /habits/{id}/ — частичное обновление,
    DELETE /habits/{id}/ — удаление.
    """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает queryset привычек, принадлежащих текущему пользователю.
        """
        return Habit.objects.filter(user=self.request.user).order_by("created_at")

    def perform_create(self, serializer):
        """
        Автоматически устанавливает пользователя при создании привычки.
        """
        serializer.save(user=self.request.user)
