from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UtilisateurViewSet

app_name = 'accounts'

router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')

urlpatterns = [
    path('auth/jeton/', TokenObtainPairView.as_view(), name='obtenir_jeton'),
    path('auth/jeton/rafraichir/', TokenRefreshView.as_view(), name='rafraichir_jeton'),
    path('', include(router.urls)),
]