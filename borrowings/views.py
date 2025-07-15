from rest_framework import viewsets

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related(
        "user", "book"
    )

    def get_serializer_class(self):
        if self.action in {"retrieve", "update", "partial_update"}:
            return BorrowingRetrieveSerializer
        return BorrowingListSerializer
