from rest_framework.permissions import BasePermission, SAFE_METHODS


class EstAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or getattr(request.user, 'role', None) == 'ADMIN'))


class EstManagerOuAdmin(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        role = getattr(request.user, 'role', None)
        return bool(request.user.is_staff or role in ('ADMIN', 'MANAGER'))


class LectureSeuleOuManagerAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return EstManagerOuAdmin().has_permission(request, view)


class EstProprietaireOuManagerAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if EstManagerOuAdmin().has_permission(request, view):
            return True
        utilisateur = getattr(obj, 'user', None) or getattr(obj, 'utilisateur', None)
        return bool(request.user and request.user.is_authenticated and utilisateur == request.user)

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)