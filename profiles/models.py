from django.db import models
from django.conf import settings


class SkillCategory(models.TextChoices):
    LANGUAGE = 'LANGUAGE', 'Langage de programmation'
    FRAMEWORK = 'FRAMEWORK', 'Framework/Technologie'
    DATABASE = 'DATABASE', 'Base de données'
    CLOUD_DEVOPS = 'CLOUD_DEVOPS', 'Cloud & DevOps'
    SPECIALIZATION = 'SPECIALIZATION', 'Spécialisation'


class Skill(models.Model):
    name = models.CharField('Nom', max_length=100, unique=True)
    category = models.CharField('Catégorie', max_length=20, choices=SkillCategory.choices)

    def __str__(self):
        return f"{self.name} ({self.category})"


class Certification(models.Model):
    issuer = models.CharField('Éditeur', max_length=100)
    name = models.CharField('Nom', max_length=150)
    issued_on = models.DateField('Délivrée le', null=True, blank=True)
    expires_on = models.DateField("Expire le", null=True, blank=True)

    class Meta:
        unique_together = ('issuer', 'name')
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'

    def __str__(self):
        return f"{self.issuer} - {self.name}"


class EngineerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='engineer_profile', verbose_name='Utilisateur')
    title = models.CharField('Intitulé', max_length=150, blank=True)
    summary = models.TextField('Résumé', blank=True)
    years_of_experience = models.PositiveIntegerField("Années d'expérience", default=0)
    location = models.CharField('Localisation', max_length=128, blank=True)
    availability = models.CharField('Disponibilité', max_length=64, default='remote', help_text='remote | on-site | hybrid')
    certifications = models.ManyToManyField(Certification, blank=True, related_name='profiles', verbose_name='Certifications')
    skills = models.ManyToManyField('Skill', through='EngineerSkill', related_name='profiles', verbose_name='Compétences')
    specializations = models.ManyToManyField('Skill', blank=True, related_name='specialized_profiles', verbose_name='Spécialisations')
    cv = models.FileField('CV', upload_to='cvs/', blank=True, null=True)

    class Meta:
        verbose_name = 'Profil Ingénieur'
        verbose_name_plural = 'Profils Ingénieurs'

    def __str__(self):
        return f"Profil de {self.user.username}"


class EngineerSkill(models.Model):
    profile = models.ForeignKey(EngineerProfile, on_delete=models.CASCADE, verbose_name='Profil')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name='Compétence')
    years_experience = models.PositiveIntegerField("Années d'expérience", default=0)
    level = models.CharField('Niveau', max_length=20, default='Intermédiaire', help_text='Junior | Intermédiaire | Senior | Lead | Architecte')

    class Meta:
        unique_together = ('profile', 'skill')
        verbose_name = 'Compétence Ingénieur'
        verbose_name_plural = 'Compétences Ingénieur'


class Experience(models.Model):
    profile = models.ForeignKey(EngineerProfile, on_delete=models.CASCADE, related_name='experiences', verbose_name='Profil')
    company = models.CharField('Entreprise', max_length=150)
    role = models.CharField('Rôle', max_length=100)
    start_date = models.DateField('Date de début')
    end_date = models.DateField('Date de fin', null=True, blank=True)
    description = models.TextField('Description', blank=True)
    technologies = models.ManyToManyField(Skill, blank=True, verbose_name='Technologies')

    class Meta:
        verbose_name = 'Expérience'
        verbose_name_plural = 'Expériences'


class PortfolioProject(models.Model):
    profile = models.ForeignKey(EngineerProfile, on_delete=models.CASCADE, related_name='portfolio', verbose_name='Profil')
    name = models.CharField('Nom', max_length=150)
    description = models.TextField('Description', blank=True)
    url = models.URLField('URL', blank=True)
    technologies = models.ManyToManyField(Skill, blank=True, verbose_name='Technologies')

    class Meta:
        verbose_name = 'Projet de Portfolio'
        verbose_name_plural = 'Projets de Portfolio'
