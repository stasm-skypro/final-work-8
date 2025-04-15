from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from habit.models import Habit
from user.models import User


@pytest.fixture
def user():
    return User.objects.create_user(
        email="testuser@example.com", first_name="Test", last_name="User", password="pass1234"
    )


@pytest.fixture
def other_user():
    return User.objects.create_user(
        email="otheruser@example.com", first_name="Other", last_name="User", password="pass1234"
    )


@pytest.fixture
def client(user):
    client = APIClient()
    client.login(email="testuser@example.com", first_name="Test", last_name="User", password="pass1234")
    return client


@pytest.fixture
def habit(user):
    return Habit.objects.create(user=user, title="Test Habit", is_public=False)


@pytest.fixture
def public_habit(other_user):
    return Habit.objects.create(user=other_user, title="Public Habit", is_public=True)


# ----------------------
# 🧪 TESTS
# ----------------------


def test_list_user_habits(client, habit):
    url = reverse("habit-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["id"] == habit.id


def test_create_habit(client):
    url = reverse("habit-list")
    data = {"title": "New Habit", "is_public": False}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Habit.objects.filter(title="New Habit").exists()


def test_retrieve_habit(client, habit):
    url = reverse("habit-detail", args=[habit.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == habit.id


def test_update_habit(client, habit):
    url = reverse("habit-detail", args=[habit.id])
    data = {"title": "Updated Title", "is_public": True}
    response = client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    habit.refresh_from_db()
    assert habit.title == "Updated Title"
    assert habit.is_public is True


def test_partial_update_habit(client, habit):
    url = reverse("habit-detail", args=[habit.id])
    data = {"title": "Partially Updated"}
    response = client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    habit.refresh_from_db()
    assert habit.title == "Partially Updated"


def test_delete_habit(client, habit):
    url = reverse("habit-detail", args=[habit.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Habit.objects.filter(id=habit.id).exists()


def test_cannot_access_other_users_habit(client, other_user):
    habit = Habit.objects.create(user=other_user, title="Other User Habit")
    url = reverse("habit-detail", args=[habit.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_public_habit_list(client, public_habit):
    url = reverse("habit-public")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert any(h["id"] == public_habit.id for h in response.data["results"])
