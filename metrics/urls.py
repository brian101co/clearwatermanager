from django.urls import path
from .views import (
    MetricTemplateView,
)

urlpatterns = [
    path('', MetricTemplateView.as_view(), name="metrics"),
]