from django.urls import include, path
from rest_framework import routers

from borrowings.views import BorrowingViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowingViewSet)

app_name = "borrowings"

urlpatterns = [
    path("", include(router.urls)),
]
