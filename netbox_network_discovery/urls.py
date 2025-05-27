from django.urls import path
from .views import discovery_view

urlpatterns = [
    path('discover/', discovery_view, name='network_discovery'),
]
