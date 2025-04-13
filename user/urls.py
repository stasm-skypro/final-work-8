from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from habit.apps import HabitConfig

from .views import LoginAPIView, RegisterAPIView

app_name = HabitConfig.name

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
]
