from django.urls import path

from .apps import HabitConfig
from .views import UserHabitListAPIView

app_name = HabitConfig.name

urlpatterns = [
    path("habits/my/", UserHabitListAPIView.as_view(), name="my-habits"),
]
