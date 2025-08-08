from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, AssignmentViewSet, SprintViewSet, MilestoneViewSet

router = DefaultRouter()
router.register(r'', ProjectViewSet, basename='project')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'sprints', SprintViewSet, basename='sprint')
router.register(r'milestones', MilestoneViewSet, basename='milestone')

urlpatterns = router.urls