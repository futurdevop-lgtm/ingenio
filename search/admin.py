from django.contrib import admin
from .models import SauvegardeRecherche


@admin.register(SauvegardeRecherche)
class SauvegardeRechercheAdmin(admin.ModelAdmin):
    list_display = ('nom', 'utilisateur', 'cree_le')
    search_fields = ('nom', 'utilisateur__username')
