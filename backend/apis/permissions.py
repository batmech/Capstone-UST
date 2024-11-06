from rest_framework import permissions

class IsBusinessOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj, action):
        # Check if the user is the owner of the business
        return obj.owner == request.user.username
