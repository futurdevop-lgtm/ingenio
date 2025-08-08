from django.db import models
from django.conf import settings
from projects.models import Project


class Ticket(models.Model):
    class Statut(models.TextChoices):
        OUVERT = 'OUVERT', 'Ouvert'
        EN_COURS = 'EN_COURS', 'En cours'
        RESOLU = 'RESOLU', 'Résolu'

    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    projet = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    rapporteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='tickets_rapportes')
    assigne_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_assignes')
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.OUVERT)
    cree_le = models.DateTimeField(auto_now_add=True)
    maj_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre


class Commentaire(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    contenu = models.TextField()
    cree_le = models.DateTimeField(auto_now_add=True)
