from decimal import Decimal

from django.db import models
from django.db.models import F, Q
from django.core.validators import MinValueValidator

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Borrowing"
        verbose_name_plural = "Borrowings"
        ordering = ("borrow_date",)
        constraints = [
            models.CheckConstraint(
                check=Q(expected_return_date__gt=F("borrow_date")),
                name="expected_return_date_after_borrow_date",
            ),
            models.CheckConstraint(
                check=Q(actual_return_date__isnull=True)
                | Q(actual_return_date__gt=F("borrow_date")),
                name="actual_return_date_after_borrow_date",
            ),
        ]

    def __str__(self):
        return (
            f"{self.user.email} (Book:{self.book.title})"
            f" (Borrowed_date: {self.borrow_date},"
            f" Expected_date: {self.expected_return_date})"
        )

    def calculate_borrowing_days(self):
        days = (self.expected_return_date - self.borrow_date).days
        return max(days, 1)

    def calculate_overdue_days(self):
        if (
            self.actual_return_date and
            self.actual_return_date.date() > self.expected_return_date
        ):
            return (self.actual_return_date.date() - self.expected_return_date).days
        return 0


class Payment(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    class PaymentTypeChoices(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    payment_status = models.CharField(
        max_length=15,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING,
    )
    payment_type = models.CharField(
        max_length=15,
        choices=PaymentTypeChoices.choices,
        default=PaymentTypeChoices.PAYMENT,
    )
    borrowing = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE
    )
    session_url = models.URLField(max_length=1000)
    session_id = models.CharField(max_length=255)
    usd_to_pay = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["usd_to_pay"]

    def __str__(self):
        return (
            f"{self.borrowing.user.email}"
            f" ({self.borrowing.book.title}) -> "
            f"{self.payment_type}"
            f" ({self.payment_status})")
