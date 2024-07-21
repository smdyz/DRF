from rest_framework.permissions import BasePermission


class IsStuff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_stuff:
            return True
        else:
            return False


class IsModer(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='moder').exists():
            return True
        return False


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user == view.get_object().owner:
            return True
        return False


class IsModerOrOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='moder').exists():
            return True
        return request.user == view.get_object().owner
