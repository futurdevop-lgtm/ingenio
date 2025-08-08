from rest_framework import serializers
from .models import Skill, Certification, EngineerProfile, EngineerSkill, Experience, PortfolioProject
from django.contrib.auth import get_user_model

User = get_user_model()


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category']


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['id', 'issuer', 'name', 'issued_on', 'expires_on']


class ExperienceSerializer(serializers.ModelSerializer):
    technologies = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Experience
        fields = ['id', 'company', 'role', 'start_date', 'end_date', 'description', 'technologies']


class PortfolioProjectSerializer(serializers.ModelSerializer):
    technologies = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = PortfolioProject
        fields = ['id', 'name', 'description', 'url', 'technologies']


class EngineerSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = EngineerSkill
        fields = ['skill', 'years_experience', 'level']


class EngineerProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    certifications = CertificationSerializer(many=True, required=False)
    skills = EngineerSkillSerializer(many=True, source='engineerskill_set', read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    portfolio = PortfolioProjectSerializer(many=True, read_only=True)

    class Meta:
        model = EngineerProfile
        fields = [
            'id', 'user', 'title', 'summary', 'years_of_experience', 'location', 'availability',
            'certifications', 'skills', 'experiences', 'portfolio', 'cv'
        ]
        read_only_fields = ['id']


class EngineerProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineerProfile
        fields = [
            'user', 'title', 'summary', 'years_of_experience', 'location', 'availability', 'cv'
        ]