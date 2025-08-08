from django.urls import path
from .views import AuditsConnexionView

urlpatterns = [
    path('audits/', AuditsConnexionView.as_view(), name='audits-connexion'),
]