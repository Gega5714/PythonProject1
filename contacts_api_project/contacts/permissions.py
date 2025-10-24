from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a contact to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the request user is the owner of the contact
        return obj.owner == request.user