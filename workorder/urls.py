from django.urls import path
from .views import (
    WorkorderListView,
    WorkorderCreateView,
    WorkorderDetailView,
    workorder_completed_view,
    WorkorderUpdateView,
    WorkorderDeleteView
)

urlpatterns = [
    path("", WorkorderListView.as_view(), name="workorder-list"),
    path("<int:id>/", WorkorderDetailView.as_view(), name="workorder-detail"),
    path("create/", WorkorderCreateView.as_view(), name="workorder-create"),
    path("edit/<int:id>/", WorkorderUpdateView.as_view(), name="workorder-update"),
    path("completed/<int:id>/", workorder_completed_view, name="workorder-completed"),
    path("delete/<int:id>/", WorkorderDeleteView.as_view(), name="workorder-delete"),
]
