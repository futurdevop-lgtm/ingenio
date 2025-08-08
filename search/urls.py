from django.urls import path
from .views import RechercheIngenieursView

urlpatterns = [
    path('ingenieurs/', RechercheIngenieursView.as_view(), name='recherche-ingenieurs'),
]