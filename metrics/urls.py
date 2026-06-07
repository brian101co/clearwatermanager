from django.urls import path
from .views import (
    MetricTemplateView,
    metrics
)

urlpatterns = [
    path('', MetricTemplateView.as_view(), name="metrics"),
    path('api/', metrics, name="api_metrics"),
]