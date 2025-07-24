from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import (
    CreateUserView,
    LogoutUserView,
    ManageUserView,
    ThrottledLoginView,
)

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="user-register"),
    path("me/", ManageUserView.as_view(), name="user-me"),
    path("logout/", LogoutUserView.as_view(), name="user-logout"),
    path("token/", ThrottledLoginView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
]
