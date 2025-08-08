from django.urls import path
from .views import EngineerSearchView

urlpatterns = [
    path('engineers/', EngineerSearchView.as_view(), name='engineer-search'),
]