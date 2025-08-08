from django.db import models
from django.conf import settings
from profiles.models import Skill, EngineerProfile


class Project(models.Model):
    class Complexity(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    domain = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=128, blank=True)
    remote_allowed = models.BooleanField(default=True)
    complexity = models.CharField(max_length=10, choices=Complexity.choices, default=Complexity.MEDIUM)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_projects')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProjectRequirement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='requirements')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    minimum_years = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=20, default='Intermediate')


class Assignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='assignments')
    engineer = models.ForeignKey(EngineerProfile, on_delete=models.CASCADE, related_name='assignments')
    allocated_percentage = models.PositiveIntegerField(default=100)
    assigned_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'engineer')


class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sprints')
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    goal = models.TextField(blank=True)


class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=150)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
