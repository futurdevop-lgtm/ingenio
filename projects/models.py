from django.db import models
from django.conf import settings
from profiles.models import Skill, EngineerProfile


class Project(models.Model):
    class Complexity(models.TextChoices):
        LOW = 'LOW', 'Faible'
        MEDIUM = 'MEDIUM', 'Moyenne'
        HIGH = 'HIGH', 'Élevée'

    name = models.CharField('Nom', max_length=150)
    description = models.TextField('Description', blank=True)
    domain = models.CharField('Domaine', max_length=100, blank=True)
    location = models.CharField('Localisation', max_length=128, blank=True)
    remote_allowed = models.BooleanField('Télétravail autorisé', default=True)
    complexity = models.CharField('Complexité', max_length=10, choices=Complexity.choices, default=Complexity.MEDIUM)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_projects', verbose_name='Créé par')
    start_date = models.DateField('Date de début', null=True, blank=True)
    end_date = models.DateField('Date de fin', null=True, blank=True)

    class Meta:
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'

    def __str__(self):
        return self.name


class ProjectRequirement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='requirements', verbose_name='Projet')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name='Compétence')
    minimum_years = models.PositiveIntegerField("Années minimales", default=0)
    level = models.CharField('Niveau', max_length=20, default='Intermédiaire')

    class Meta:
        verbose_name = 'Exigence du projet'
        verbose_name_plural = 'Exigences du projet'


class Assignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='assignments', verbose_name='Projet')
    engineer = models.ForeignKey(EngineerProfile, on_delete=models.CASCADE, related_name='assignments', verbose_name='Ingénieur')
    allocated_percentage = models.PositiveIntegerField('Pourcentage alloué', default=100)
    assigned_on = models.DateField('Assigné le', auto_now_add=True)

    class Meta:
        unique_together = ('project', 'engineer')
        verbose_name = 'Affectation'
        verbose_name_plural = 'Affectations'


class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sprints', verbose_name='Projet')
    name = models.CharField('Nom', max_length=100)
    start_date = models.DateField('Date de début')
    end_date = models.DateField('Date de fin')
    goal = models.TextField('Objectif', blank=True)

    class Meta:
        verbose_name = 'Sprint'
        verbose_name_plural = 'Sprints'


class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones', verbose_name='Projet')
    name = models.CharField('Nom', max_length=150)
    due_date = models.DateField('Échéance')
    completed = models.BooleanField('Terminé', default=False)

    class Meta:
        verbose_name = 'Jalon'
        verbose_name_plural = 'Jalons'
