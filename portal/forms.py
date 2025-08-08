from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from profiles.models import EngineerProfile
from projects.models import Project

User = get_user_model()


class EngineerProfileForm(forms.ModelForm):
    class Meta:
        model = EngineerProfile
        fields = ['title', 'summary', 'years_of_experience', 'location', 'availability', 'cv']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'domain', 'location', 'remote_allowed', 'complexity', 'start_date', 'end_date']


class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")