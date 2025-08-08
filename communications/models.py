from django.db import models
from django.conf import settings


class Notification(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField('Titre', max_length=150)
    message = models.TextField('Message')
    lu = models.BooleanField('Lu', default=False)
    cree_le = models.DateTimeField('Créé le', auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"{self.titre}"
