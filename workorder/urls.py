from django.urls import path
from .views import (
    WorkorderListView,
    WorkorderCreateView,
    WorkorderDetailView
)

urlpatterns = [
    path("", WorkorderListView.as_view(), name="workorder-list"),
    path("<int:id>/", WorkorderDetailView.as_view(), name="workorder-detail"),
    path("create/", WorkorderCreateView.as_view(), name="workorder-create"),
]
