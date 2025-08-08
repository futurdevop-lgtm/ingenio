from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Assignment, Sprint, Milestone
from .serializers import ProjectSerializer, AssignmentSerializer, SprintSerializer, MilestoneSerializer
from profiles.models import EngineerProfile


# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related('requirements')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['domain', 'location', 'complexity', 'remote_allowed']
    search_fields = ['name', 'description']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'])
    def match(self, request, pk=None):
        project = self.get_object()
        required_skills = {req.skill_id: (req.minimum_years, req.level) for req in project.requirements.all()}
        candidates = EngineerProfile.objects.prefetch_related('skills').all()
        results = []
        for profile in candidates:
            score = 0
            skills_map = {es.skill_id: (es.years_experience, es.level) for es in profile.engineerskill_set.all()}
            for skill_id, (min_years, _level) in required_skills.items():
                if skill_id in skills_map and skills_map[skill_id][0] >= min_years:
                    score += 1
            if score:
                results.append({'profile_id': profile.id, 'user': profile.user.username, 'score': score})
        results.sort(key=lambda x: x['score'], reverse=True)
        return Response(results)


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related('project', 'engineer').all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        serializer.save(project_id=project_id)


class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.select_related('project').all()
    serializer_class = SprintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(project_id=self.request.data.get('project'))


class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.select_related('project').all()
    serializer_class = MilestoneSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(project_id=self.request.data.get('project'))
