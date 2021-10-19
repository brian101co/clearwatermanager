from django.urls import path
from .views import (
    WorkOrderListView
)

urlpatterns = [
    path("", WorkOrderListView.as_view(), name="workorder-list"),
]
