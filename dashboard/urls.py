from django.urls import path
from .views import TableauManagerView

app_name = 'dashboard'

urlpatterns = [
    path('manager/', TableauManagerView.as_view(), name='tableau-manager'),
]