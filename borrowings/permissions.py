from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsBorrowingOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

class IsAdminOrIsAuthenticatedOnlyCreate(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.is_staff or request.method in SAFE_METHODS or request.method == "POST"
        return False
