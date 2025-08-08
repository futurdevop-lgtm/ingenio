from django.urls import path
from .views import ManagerDashboardView

urlpatterns = [
    path('manager/', ManagerDashboardView.as_view(), name='manager-dashboard'),
]