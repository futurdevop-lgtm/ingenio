from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrateur'
        MANAGER = 'MANAGER', 'Manager'
        ENGINEER = 'ENGINEER', 'Ingénieur'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ENGINEER,
        help_text='Rôle de l’utilisateur dans la plateforme'
    )
    phone_number = models.CharField('Numéro de téléphone', max_length=32, blank=True)
    location = models.CharField('Localisation', max_length=128, blank=True)

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
