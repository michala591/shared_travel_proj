from rest_framework.permissions import BasePermission


class IsDriverUser(BasePermission):
    """
    Custom permission to only allow users who are drivers to access the view.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "DR"


class IsPassengerUser(BasePermission):
    """
    Custom permission to only allow users who are passengers to access the view.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "PR"
