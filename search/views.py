from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from profiles.models import EngineerProfile, Skill, EngineerSkill
from profiles.serializers import EngineerProfileSerializer


# Create your views here.

class RechercheIngenieursView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = EngineerProfile.objects.select_related('user').prefetch_related('skills', 'certifications')

        pile = request.query_params.get('pile')  # MEAN, LAMP, .NET, etc.
        niveau = request.query_params.get('niveau')  # Junior, Senior, Lead, Architecte
        domaine = request.query_params.get('domaine')  # web, mobile, data science, cybersécurité
        disponibilite = request.query_params.get('disponibilite')  # remote/on-site/hybrid
        localisation = request.query_params.get('localisation')
        competences = request.query_params.getlist('competence')  # noms multiples
        min_annees = request.query_params.get('min_annees')

        if disponibilite:
            queryset = queryset.filter(availability__iexact=disponibilite)
        if localisation:
            queryset = queryset.filter(location__icontains=localisation)
        if niveau:
            queryset = queryset.filter(engineerskill__level__iexact=niveau)
        if min_annees:
            queryset = queryset.filter(engineerskill__years_experience__gte=int(min_annees))
        if domaine:
            queryset = queryset.filter(Q(title__icontains=domaine) | Q(summary__icontains=domaine))
        if pile:
            stacks = {
                'MEAN': ['MongoDB', 'Express', 'Angular', 'Node.js'],
                'MERN': ['MongoDB', 'Express', 'React', 'Node.js'],
                'LAMP': ['Linux', 'Apache', 'MySQL', 'PHP'],
                '.NET': ['C#', 'ASP.NET', 'SQL Server'],
            }
            for skill_name in stacks.get(pile.upper(), []):
                queryset = queryset.filter(skills__name__iexact=skill_name)
        for s in competences:
            queryset = queryset.filter(skills__name__iexact=s)

        queryset = queryset.distinct()
        serializer = EngineerProfileSerializer(queryset, many=True)
        return Response(serializer.data)
