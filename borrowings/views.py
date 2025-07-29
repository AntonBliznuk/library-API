from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from borrowings.models import Borrowing, Payment
from borrowings.permissions import IsAdminOrIsAuthenticatedOnlyCreate, IsBorrowingOwner
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
    PaymentListSerializer,
    PaymentRetrieveSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user", "book")
    permission_classes = [IsAdminOrIsAuthenticatedOnlyCreate]

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("user", "book")

        is_active = self.request.query_params.get("is_active")
        if is_active == "true":
            queryset = queryset.filter(actual_return_date=None)
        elif is_active == "false":
            queryset = queryset.exclude(actual_return_date=None)

        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def get_serializer_class(self):
        if self.action in {"retrieve", "update", "partial_update"}:
            return BorrowingRetrieveSerializer
        return BorrowingListSerializer

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsBorrowingOwner],
        url_path="return_borrowing",
    )
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.actual_return_date is not None:
            return Response(
                {"message": "This book is already returned."},
                status=status.HTTP_409_CONFLICT,
            )

        book = borrowing.book
        book.inventory += 1
        book.save()

        if borrowing.borrow_date >= timezone.now().date():
            return Response(
                {"message": "This book is not borrowed yet."},
                status=status.HTTP_409_CONFLICT,
            )

        borrowing.actual_return_date = timezone.now()
        borrowing.save()

        return Response(
            {"message": "This book is now returned."}, status=status.HTTP_200_OK
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                description="Whether the borrowings is active or not.",
                type=OpenApiTypes.BOOL,
            ),
            OpenApiParameter(
                name="user_id",
                description="The ID of the user who"
                            " owns the borrowing (only for admins).",
                type=OpenApiTypes.INT,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("borrowing")
    permission_classes = [IsAuthenticated]
    allowed_methods = ["get"]

    def get_serializer_class(self):
        if self.action in {"retrieve", "update", "partial_update"}:
            return PaymentRetrieveSerializer
        return PaymentListSerializer

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = queryset.filter(
                borrowing__user=self.request.user,
            )

        return queryset
