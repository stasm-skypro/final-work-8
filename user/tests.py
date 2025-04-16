from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User


class UserTests(APITestCase):
    def setUp(self):
        self.registration_url = reverse("user:register")  # убедись, что имя url задан
        self.login_url = reverse("user:login")  # и тут тоже
        self.user_data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "StrongPassword123",
        }

    def test_user_registration(self):
        response = self.client.post(self.registration_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_data["email"]).exists())

    def test_user_login_with_valid_credentials(self):
        User.objects.create_user(**self.user_data)
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_login_with_invalid_credentials(self):
        User.objects.create_user(**self.user_data)
        login_data = {
            "email": self.user_data["email"],
            "password": "WrongPassword",
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Неверный email или пароль.")

    def test_user_str_representation(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data["email"])
