from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    """Разрешает изменения только админу."""

    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
        )


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Разрешает просмотр всем, изменения - только админу."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
            or request.user.is_authenticated and request.user.is_staff
        )


class IsOwnerAdminModeratorOrReadOnly(permissions.BasePermission):
    """Разрешает изменение только автору, модератору или админу."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
