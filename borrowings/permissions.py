from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsBorrowingOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user