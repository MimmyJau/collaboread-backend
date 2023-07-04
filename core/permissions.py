from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission where anyone can read but only owners can write.
    """

    def has_object_permission(self, request, view, obj):
        """
        According to docs, .has_object_permission() is not called
        automatically on every object when a list is returned, thus
        this method is not called for list views by default.
        Source: https://www.django-rest-framework.org/api-guide/permissions/#limitations-of-object-level-permissions
        """
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user


class IsOwnerOnly(permissions.BasePermission):
    """
    Custom permission where only owners can read or write.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
