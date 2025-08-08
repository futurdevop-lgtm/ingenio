from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, TwoFASetupSerializer, TwoFAVerifySerializer
from security.permissions import EstAdmin, EstProprietaireOuManagerAdmin
import pyotp

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

    @action(detail=False, methods=['post'], url_path='2fa/demarrer')
    def deuxfa_demarrer(self, request):
        user = request.user
        secret = pyotp.random_base32()
        user.two_factor_secret = secret
        user.save(update_fields=['two_factor_secret'])
        otp_auth_url = pyotp.totp.TOTP(secret).provisioning_uri(name=user.email or user.username, issuer_name='PlateformeTalents')
        return Response({'secret': secret, 'otp_auth_url': otp_auth_url})

    @action(detail=False, methods=['post'], url_path='2fa/activer')
    def deuxfa_activer(self, request):
        serializer = TwoFAVerifySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.two_factor_enabled = True
        user.save(update_fields=['two_factor_enabled'])
        return Response({'detail': '2FA activée'})

    @action(detail=False, methods=['post'], url_path='2fa/desactiver')
    def deuxfa_desactiver(self, request):
        user = request.user
        user.two_factor_enabled = False
        user.two_factor_secret = ''
        user.save(update_fields=['two_factor_enabled', 'two_factor_secret'])
        return Response({'detail': '2FA désactivée'})
