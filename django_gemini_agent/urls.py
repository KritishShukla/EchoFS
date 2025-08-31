from django.urls import path, include

urlpatterns = [
    path('api/agent/', include('apps.agent.urls')),
]