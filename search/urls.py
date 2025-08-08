from django.urls import path
from .views import RechercheIngenieursView

app_name = 'search'

urlpatterns = [
    path('ingenieurs/', RechercheIngenieursView.as_view(), name='recherche-ingenieurs'),
]