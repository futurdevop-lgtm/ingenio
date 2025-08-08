from rest_framework.routers import DefaultRouter
from .views import ProjetViewSet, AffectationViewSet, SprintViewSet, JalonViewSet

router = DefaultRouter()
router.register(r'', ProjetViewSet, basename='projet')
router.register(r'affectations', AffectationViewSet, basename='affectation')
router.register(r'sprints', SprintViewSet, basename='sprint')
router.register(r'jalons', JalonViewSet, basename='jalon')

urlpatterns = router.urls