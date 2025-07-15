from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.permissions import IsBorrowingOwner
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related(
        "user", "book"
    )
    permission_classes = [IsAuthenticated]

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
                status=status.HTTP_409_CONFLICT
            )

        book = borrowing.book
        book.inventory += 1
        book.save()

        if borrowing.borrow_date >= timezone.now().date():
            return Response(
                {"message": "This book is not borrowed yet."},
                status=status.HTTP_409_CONFLICT
            )

        borrowing.actual_return_date = timezone.now()
        borrowing.save()

        return Response(
            {"message": "This book is now returned."},
            status=status.HTTP_200_OK
        )
