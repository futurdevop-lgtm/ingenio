from django.shortcuts import render
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from security.permissions import LectureSeuleOuManagerAdmin, EstProprietaireOuManagerAdmin
from .models import Skill, Certification, EngineerProfile
from .serializers import (
    SkillSerializer,
    CertificationSerializer,
    EngineerProfileSerializer,
    EngineerProfileCreateUpdateSerializer,
)


# Create your views here.


class CompetenceViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by('name')
    serializer_class = SkillSerializer
    permission_classes = [LectureSeuleOuManagerAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'name']
    search_fields = ['name']


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all().order_by('issuer')
    serializer_class = CertificationSerializer
    permission_classes = [LectureSeuleOuManagerAdmin]
    search_fields = ['issuer', 'name']


class ProfilIngenieurViewSet(viewsets.ModelViewSet):
    queryset = EngineerProfile.objects.select_related('user').prefetch_related('certifications', 'skills').all()
    permission_classes = [EstProprietaireOuManagerAdmin]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['availability', 'location']
    search_fields = ['user__username', 'title', 'summary']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EngineerProfileCreateUpdateSerializer
        return EngineerProfileSerializer
