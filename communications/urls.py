from django.urls import path
from .views import NotificationsView

app_name = 'communications'

urlpatterns = [
    path('notifications/', NotificationsView.as_view(), name='notifications'),
]