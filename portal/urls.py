from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.accueil_app, name='accueil-app'),
    path('tableau/', views.tableau, name='tableau'),
    path('profils/', views.profils, name='profils'),
    path('projets/', views.projets, name='projets'),
    path('recherche/', views.recherche, name='recherche'),
]