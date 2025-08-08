from django.db import models
from django.conf import settings


class SkillCategory(models.TextChoices):
    LANGUAGE = 'LANGUAGE', 'Programming Language'
    FRAMEWORK = 'FRAMEWORK', 'Framework/Technology'
    DATABASE = 'DATABASE', 'Database'
    CLOUD_DEVOPS = 'CLOUD_DEVOPS', 'Cloud & DevOps'
    SPECIALIZATION = 'SPECIALIZATION', 'Specialization'


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=SkillCategory.choices)

    def __str__(self):
        return f"{self.name} ({self.category})"


class Certification(models.Model):
    issuer = models.CharField(max_length=100)
    name = models.CharField(max_length=150)
    issued_on = models.DateField(null=True, blank=True)
    expires_on = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('issuer', 'name')

    def __str__(self):
        return f"{self.issuer} - {self.name}"


class EngineerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='engineer_profile')
    title = models.CharField(max_length=150, blank=True)
    summary = models.TextField(blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=128, blank=True)
    availability = models.CharField(max_length=64, default='remote', help_text='remote | on-site | hybrid')
    certifications = models.ManyToManyField(Certification, blank=True, related_name='profiles')
    skills = models.ManyToManyField(Skill, through='EngineerSkill', related_name='profiles')
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class EngineerSkill(models.Model):
    profile = models.ForeignKey(EngineerProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    years_experience = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=20, default='Intermediate', help_text='Junior | Intermediate | Senior | Lead | Architect')

    class Meta:
        unique_together = ('profile', 'skill')


class Experience(models.Model):
    profile = models.ForeignKey(EngineerProfile, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    technologies = models.ManyToManyField(Skill, blank=True)


class PortfolioProject(models.Model):
    profile = models.ForeignKey(EngineerProfile, on_delete=models.CASCADE, related_name='portfolio')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    technologies = models.ManyToManyField(Skill, blank=True)
