from django import forms
from .models import Ticket, Commentaire


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titre', 'description', 'projet', 'assigne_a', 'statut']


class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['contenu']