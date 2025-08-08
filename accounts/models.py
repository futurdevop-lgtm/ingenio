from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        ENGINEER = 'ENGINEER', 'Engineer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ENGINEER,
    )
    phone_number = models.CharField(max_length=32, blank=True)
    location = models.CharField(max_length=128, blank=True)

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
