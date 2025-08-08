from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from profiles.models import EngineerProfile, Skill, EngineerSkill
from profiles.serializers import EngineerProfileSerializer


# Create your views here.

class EngineerSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = EngineerProfile.objects.select_related('user').prefetch_related('skills', 'certifications')

        stack = request.query_params.get('stack')  # MEAN, LAMP, .NET, etc.
        level = request.query_params.get('level')  # Junior, Senior, Lead, Architect
        domain = request.query_params.get('domain')  # web, mobile, data science, cybersecurity
        availability = request.query_params.get('availability')  # remote/on-site/hybrid
        location = request.query_params.get('location')
        skills = request.query_params.getlist('skill')  # multiple skill names
        min_years = request.query_params.get('min_years')

        if availability:
            queryset = queryset.filter(availability__iexact=availability)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if level:
            queryset = queryset.filter(engineerskill__level__iexact=level)
        if min_years:
            queryset = queryset.filter(engineerskill__years_experience__gte=int(min_years))
        if domain:
            # naive domain matching via profile title/summary
            queryset = queryset.filter(Q(title__icontains=domain) | Q(summary__icontains=domain))
        if stack:
            stacks = {
                'MEAN': ['MongoDB', 'Express', 'Angular', 'Node.js'],
                'MERN': ['MongoDB', 'Express', 'React', 'Node.js'],
                'LAMP': ['Linux', 'Apache', 'MySQL', 'PHP'],
                '.NET': ['C#', 'ASP.NET', 'SQL Server'],
            }
            for skill_name in stacks.get(stack.upper(), []):
                queryset = queryset.filter(skills__name__iexact=skill_name)
        for s in skills:
            queryset = queryset.filter(skills__name__iexact=s)

        queryset = queryset.distinct()
        serializer = EngineerProfileSerializer(queryset, many=True)
        return Response(serializer.data)
