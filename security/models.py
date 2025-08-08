from django.db import models
from django.conf import settings

# Create your models here.


class AuditConnexion(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Utilisateur')
    adresse_ip = models.GenericIPAddressField('Adresse IP', null=True, blank=True)
    user_agent = models.CharField('Agent utilisateur', max_length=512, blank=True)
    succes = models.BooleanField('Succès', default=False)
    cree_le = models.DateTimeField('Créé le', auto_now_add=True)

    class Meta:
        verbose_name = 'Traçabilité de connexion'
        verbose_name_plural = 'Traçabilité des connexions'

    def __str__(self):
        return f"Audit {self.utilisateur} @ {self.cree_le}"
