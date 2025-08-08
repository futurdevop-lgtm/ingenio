from rest_framework.routers import DefaultRouter
from .views import SkillViewSet, CertificationViewSet, EngineerProfileViewSet

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'certifications', CertificationViewSet, basename='cert')
router.register(r'profiles', EngineerProfileViewSet, basename='profile')

urlpatterns = router.urls