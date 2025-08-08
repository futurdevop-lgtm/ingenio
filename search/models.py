from django.db import models
from django.conf import settings


class SauvegardeRecherche(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recherches')
    nom = models.CharField('Nom', max_length=150)
    criteres = models.JSONField('Critères')
    cree_le = models.DateTimeField('Créé le', auto_now_add=True)

    class Meta:
        verbose_name = 'Recherche sauvegardée'
        verbose_name_plural = 'Recherches sauvegardées'

    def __str__(self):
        return self.nom
