from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count
from profiles.models import EngineerProfile
from projects.models import Project, Assignment


class ManagerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_engineers = EngineerProfile.objects.count()
        total_projects = Project.objects.count()
        active_assignments = Assignment.objects.count()
        avg_experience = EngineerProfile.objects.aggregate(avg=Avg('years_of_experience'))['avg'] or 0

        data = {
            'kpis': {
                'total_engineers': total_engineers,
                'total_projects': total_projects,
                'active_assignments': active_assignments,
                'avg_experience_years': round(avg_experience, 2),
            }
        }
        return Response(data)
