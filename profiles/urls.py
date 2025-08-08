from rest_framework.routers import DefaultRouter
from .views import CompetenceViewSet, CertificationViewSet, ProfilIngenieurViewSet

app_name = 'profiles'

router = DefaultRouter()
router.register(r'competences', CompetenceViewSet, basename='competence')
router.register(r'certifications', CertificationViewSet, basename='certification')
router.register(r'ingenieurs', ProfilIngenieurViewSet, basename='profil-ingenieur')

urlpatterns = router.urls