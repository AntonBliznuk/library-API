from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books.models import Book
from books.serializers import BookSerializer
from borrowings.models import Borrowing, Payment
from users.serializers import UserSerializer

from utils.stripe import create_stripe_session_for_borrowing


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
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user_email",
            "book_title",
            "book_id",
        )
        read_only_fields = ("id", "actual_return_date")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        book = attrs["book_id"]
        if book.inventory <= 0:
            raise ValidationError(
                {
                    "book_id": "This book is not available.",
                }
            )
        if attrs["borrow_date"] > attrs["expected_return_date"]:
            raise ValidationError(
                {
                    "expected_return_date":
                        "Expected return date must come after borrowing date.",
                }
            )

        return attrs

    def create(self, validated_data):
        book = validated_data.pop("book_id")
        user = self.context["request"].user

        book.inventory -= 1
        book.save()

        borrowing = Borrowing.objects.create(book=book, user=user, **validated_data)

        create_stripe_session_for_borrowing(borrowing, self.context["request"])

        return borrowing


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "payment_status",
            "payment_type",
            "session_url",
            "session_id",
            "usd_to_pay",
        )


class PaymentListSerializer(serializers.ModelSerializer):
    borrowing = BorrowingListSerializer(read_only=True)
    borrowing_id = serializers.PrimaryKeyRelatedField(
        queryset=Borrowing.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Payment
        fields = (
            "id",
            "payment_status",
            "payment_type",
            "borrowing_id",
            "borrowing",
            "session_url",
            "session_id",
            "usd_to_pay",
        )
        read_only_fields = (
            "id",
            "payment_status",
            "payment_type",
            "borrowing_id",
            "borrowing",
            "session_url",
            "session_id",
            "usd_to_pay",
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        borrowing = attrs.get("borrowing_id")
        payment_type = attrs.get("payment_type")
        payment_status = Payment.PaymentStatusChoices.PENDING

        if Payment.objects.filter(
            borrowing=borrowing,
            payment_status=payment_status,
            payment_type=payment_type,
        ).exists():
            raise ValidationError(
                f"A pending payment of type '{payment_type}' "
                f"already exists for this borrowing."
            )
        return attrs


    def create(self, validated_data):
        borrowing = validated_data.pop("borrowing_id")
        payment = Payment.objects.create(
            borrowing=borrowing,
            **validated_data
        )
        return payment


class BorrowingRetrieveSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    payments = PaymentSerializer(
        many=True, read_only=True, source="payment_set"
    )

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user",
            "book",
            "payments",
        )
        read_only_fields = (
            "id",
            "actual_return_date",
        )


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    borrowing = BorrowingListSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "payment_status",
            "payment_type",
            "borrowing",
            "session_url",
            "session_id",
            "usd_to_pay",
        )
        read_only_fields = (
            "id",
            "payment_status",
            "payment_type",
            "session_url",
            "session_id",
            "usd_to_pay",
        )
