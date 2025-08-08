from rest_framework import serializers
from profiles.serializers import SkillSerializer, EngineerProfileSerializer
from .models import Project, ProjectRequirement, Assignment, Sprint, Milestone
from profiles.models import EngineerProfile, Skill


class ProjectRequirementSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), source='skill', write_only=True)

    class Meta:
        model = ProjectRequirement
        fields = ['id', 'skill', 'skill_id', 'minimum_years', 'level']


class ProjectSerializer(serializers.ModelSerializer):
    requirements = ProjectRequirementSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'domain', 'location', 'remote_allowed', 'complexity', 'created_by', 'start_date', 'end_date', 'requirements']
        read_only_fields = ['id', 'created_by']

    def create(self, validated_data):
        requirements_data = validated_data.pop('requirements', [])
        project = Project.objects.create(**validated_data)
        for req in requirements_data:
            ProjectRequirement.objects.create(project=project, **req)
        return project

    def update(self, instance, validated_data):
        requirements_data = validated_data.pop('requirements', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if requirements_data is not None:
            instance.requirements.all().delete()
            for req in requirements_data:
                ProjectRequirement.objects.create(project=instance, **req)
        return instance


class AssignmentSerializer(serializers.ModelSerializer):
    engineer = EngineerProfileSerializer(read_only=True)
    engineer_id = serializers.PrimaryKeyRelatedField(queryset=EngineerProfile.objects.all(), source='engineer', write_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'project', 'engineer', 'engineer_id', 'allocated_percentage', 'assigned_on']
        read_only_fields = ['id', 'assigned_on', 'project']


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ['id', 'project', 'name', 'start_date', 'end_date', 'goal']
        read_only_fields = ['id', 'project']


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ['id', 'project', 'name', 'due_date', 'completed']
        read_only_fields = ['id', 'project']


class ChargeTravailSerializer(serializers.Serializer):
    profil_id = serializers.IntegerField()
    utilisateur = serializers.CharField()
    charge_totale = serializers.IntegerField(help_text='Somme des pourcentages alloués sur les affectations actives')