from django.urls import path
from .views import AuditsConnexionView

app_name = 'security'

urlpatterns = [
    path('audits/', AuditsConnexionView.as_view(), name='audits-connexion'),
]