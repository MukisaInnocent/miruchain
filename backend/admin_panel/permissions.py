"""
Custom permission classes for admin endpoints.
"""
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    """
    
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_admin or request.user.is_superuser or request.user.is_staff)
        )
