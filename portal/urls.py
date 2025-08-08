from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.accueil_app, name='accueil-app'),
    path('inscription/', views.inscription, name='inscription'),
    path('tableau/', views.tableau, name='tableau'),
    path('profils/', views.profils, name='profils'),
    path('profils/creer/', views.profil_creer, name='profil-creer'),
    path('profils/<int:profil_id>/editer/', views.profil_editer, name='profil-editer'),
    path('profils/<int:profil_id>/supprimer/', views.profil_supprimer, name='profil-supprimer'),
    path('projets/', views.projets, name='projets'),
    path('projets/creer/', views.projet_creer, name='projet-creer'),
    path('projets/<int:projet_id>/editer/', views.projet_editer, name='projet-editer'),
    path('projets/<int:projet_id>/supprimer/', views.projet_supprimer, name='projet-supprimer'),
    path('recherche/', views.recherche, name='recherche'),
    path('login/', auth_views.LoginView.as_view(template_name='portal/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]