from django.urls import path
from . import views

app_name = 'issues'

urlpatterns = [
    path('', views.tickets_liste, name='tickets'),
    path('creer/', views.ticket_creer, name='ticket-creer'),
    path('<int:ticket_id>/editer/', views.ticket_editer, name='ticket-editer'),
    path('<int:ticket_id>/supprimer/', views.ticket_supprimer, name='ticket-supprimer'),
]