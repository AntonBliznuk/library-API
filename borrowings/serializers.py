from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.serializers import UserSerializer
from books.serializers import BookSerializer

from books.models import Book
from borrowings.models import Borrowing


class BorrowingListSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    book_title = serializers.CharField(source="book.title", read_only=True)

    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user_email",
            "book_title",
            "book_id",
        )
        read_only_fields = (
            "id",
            "actual_return_date"
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        book = attrs["book_id"]
        if book.inventory <= 0:
            raise ValidationError({
                "book_id": "This book is not available.",
            })
        if attrs["borrow_date"] > attrs["expected_return_date"]:
            raise ValidationError({
                "expected_return_date": "Expected return date must come after borrowing date.",
            })

        return attrs

    def create(self, validated_data):
        book = validated_data.pop("book_id")
        user = self.context["request"].user

        book.inventory -= 1
        book.save()

        borrowing = Borrowing.objects.create(book=book, user=user, **validated_data)
        return borrowing


class BorrowingRetrieveSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user",
            "book"
        )
        read_only_fields = (
            "id",
            "actual_return_date",
        )
