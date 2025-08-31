from django.urls import path
from .views import CommandView

urlpatterns = [
    path('command/', CommandView.as_view(), name='agent-command'),
]