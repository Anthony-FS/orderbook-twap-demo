from django.urls import path

from core.views import HealthView

urlpatterns = [
    path("api/health/", HealthView.as_view()),
]
