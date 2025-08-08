from django import forms
from profiles.models import EngineerProfile
from projects.models import Project


class EngineerProfileForm(forms.ModelForm):
    class Meta:
        model = EngineerProfile
        fields = ['title', 'summary', 'years_of_experience', 'location', 'availability', 'cv']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'domain', 'location', 'remote_allowed', 'complexity', 'start_date', 'end_date']