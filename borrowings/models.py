from django.db import models
from django.db.models import Q, F

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
        ordering = ("borrow_date", )
        constraints = [
            models.CheckConstraint(
                check=Q(expected_return_date__gt=F("borrow_date")),
                name="expected_return_date_after_borrow_date",
            ),
            models.CheckConstraint(
                check=Q(actual_return_date__isnull=True) | Q(actual_return_date__gt=F("borrow_date")),
                name="actual_return_date_after_borrow_date",
            ),
        ]

    def __str__(self):
        return (
            f"{self.user.email} (Book:{self.book.title})"
            f" (Borrowed_date: {self.borrow_date},"
            f" Expected_date: {self.expected_return_date})"
        )
