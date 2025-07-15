from rest_framework import serializers

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

    def create(self, validated_data):
        book = validated_data.pop("book_id")
        user = self.context["request"].user
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
