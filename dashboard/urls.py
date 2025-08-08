from django.urls import path
from .views import TableauManagerView

urlpatterns = [
    path('manager/', TableauManagerView.as_view(), name='tableau-manager'),
]