from django.urls import include, path
from rest_framework import routers

from borrowings.views import (
    BorrowingViewSet,
    PaymentViewSet
)

router = routers.DefaultRouter()
router.register("borrowings", BorrowingViewSet)
router.register("payments", PaymentViewSet)

app_name = "borrowings"

urlpatterns = [
    path("", include(router.urls)),
]
