from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer
from security.permissions import EstAdmin, EstProprietaireOuManagerAdmin

User = get_user_model()


class EstLuiMemeOuAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['id', 'username']

    def get_permissions(self):
        if self.action in ['create', 'inscription']:
            return [permissions.AllowAny()]
        if self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [EstProprietaireOuManagerAdmin]
        elif self.action in ['list', 'destroy']:
            self.permission_classes = [EstAdmin]
        return super().get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny], url_path='inscription')
    def inscription(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='moi')
    def moi(self, request):
        return Response(UserSerializer(request.user).data)
