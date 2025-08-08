from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from profiles.models import EngineerProfile
from projects.models import Project, Assignment


class TableauManagerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_ingenieurs = EngineerProfile.objects.count()
        total_projets = Project.objects.count()
        affectations_actives = Assignment.objects.count()
        experience_moyenne = EngineerProfile.objects.aggregate(avg=Avg('years_of_experience'))['avg'] or 0

        data = {
            'kpis': {
                'total_ingenieurs': total_ingenieurs,
                'total_projets': total_projets,
                'affectations_actives': affectations_actives,
                'experience_moyenne_annees': round(experience_moyenne, 2),
            }
        }
        return Response(data)
