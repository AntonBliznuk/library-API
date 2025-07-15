from django.test import TestCase
from django.contrib.auth import get_user_model
from books.models import Book
from borrowings.models import Borrowing
from datetime import date

User = get_user_model()

class BorrowingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Soft",
            inventory=2,
            daily_fee=1.5,
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            borrow_date=date(2025, 7, 10),
            expected_return_date=date(2025, 7, 20)
        )

    def test_borrowing_str(self):
        expected_str = (
            f"{self.user.email} (Book:{self.book.title})"
            f" (Borrowed_date: {self.borrowing.borrow_date},"
            f" Expected_date: {self.borrowing.expected_return_date})"
        )
        self.assertEqual(str(self.borrowing), expected_str)


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from borrowings.models import Borrowing
from books.models import Book  # Adjust if Book model is elsewhere
from datetime import date
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class BorrowingViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password123"
        )
        self.admin = User.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=3,
            daily_fee=1.5,
        )

        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            borrow_date=date(2025, 7, 1),
            expected_return_date=date(2025, 7, 10),
        )

        self.url_list = reverse("borrowings:borrowing-list")
        self.url_detail = reverse("borrowings:borrowing-detail", args=[self.borrowing.id])
        self.url_return = reverse("borrowings:borrowing-return-borrowing", args=[self.borrowing.id])

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {refresh.access_token}")

    def test_list_as_admin(self):
        self.authenticate(self.admin)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_as_user(self):
        self.authenticate(self.user)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_filter_is_active_true(self):
        self.authenticate(self.user)
        response = self.client.get(self.url_list, {"is_active": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_filter_is_active_false(self):
        self.borrowing.actual_return_date = date(2025, 7, 15)
        self.borrowing.save()

        self.authenticate(self.user)
        response = self.client.get(self.url_list, {"is_active": "false"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_return_borrowing_success(self):
        self.authenticate(self.user)
        response = self.client.post(self.url_return)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.borrowing.refresh_from_db()
        self.assertIsNotNone(self.borrowing.actual_return_date)

    def test_return_borrowing_already_returned(self):
        self.borrowing.actual_return_date = date(2025, 7, 15)
        self.borrowing.save()

        self.authenticate(self.user)
        response = self.client.post(self.url_return)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_permission_only_owner_can_return(self):
        other_user = User.objects.create_user(email="other@example.com", password="pass")
        self.authenticate(other_user)
        response = self.client.post(self.url_return)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_unauthorized(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
