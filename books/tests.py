from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from books.models import Book

User = get_user_model()


def get_jwt_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class BookViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )
        self.regular_user = User.objects.create_user(
            email="user@example.com", password="userpass"
        )

        self.book = Book.objects.create(
            title="Refactoring",
            author="Martin Fowler",
            cover=Book.CoverChoices.HARD,
            inventory=10,
            daily_fee="3.99",
        )

        self.list_url = reverse("books:book-list")
        self.detail_url = reverse("books:book-detail", args=[self.book.id])

    def test_list_books_as_anonymous(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_book_as_anonymous(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_create_book_as_admin(self):
        token = get_jwt_token_for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {token['access']}")

        data = {
            "title": "The Mythical Man-Month",
            "author": "Fred Brooks",
            "cover": Book.CoverChoices.SOFT,
            "inventory": 5,
            "daily_fee": "1.99",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_as_regular_user_forbidden(self):
        token = get_jwt_token_for_user(self.regular_user)
        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {token['access']}")

        data = {
            "title": "The Mythical Man-Month",
            "author": "Fred Brooks",
            "cover": Book.CoverChoices.SOFT,
            "inventory": 5,
            "daily_fee": "1.99",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_as_admin(self):
        token = get_jwt_token_for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {token['access']}")

        data = {"title": "Refactoring 2nd Edition"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Refactoring 2nd Edition")

    def test_delete_book_as_admin(self):
        token = get_jwt_token_for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {token['access']}")

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_as_regular_user_forbidden(self):
        token = get_jwt_token_for_user(self.regular_user)
        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {token['access']}")

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BookModelTest(TestCase):
    def test_str_method_returns_title_and_author(self):
        book = Book.objects.create(
            title="Clean Code",
            author="Robert C. Martin",
            cover=Book.CoverChoices.HARD,
            inventory=5,
            daily_fee="2.50",
        )

        expected_str = "Clean Code (author: Robert C. Martin)"
        self.assertEqual(str(book), expected_str)
