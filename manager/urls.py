from django.urls import path
from .views import (
    MetricTemplateView,
    DashboardHomeView,
    DashboardLoginView,
    ReservationDetailView,
    DeleteReservationView,
    CreateReservationView,
    EditReservationView,
    getAvaliability
)

urlpatterns = [
    path('', DashboardLoginView.as_view(), name="loginuser"),
    path('dashboard/', DashboardHomeView.as_view(), name='home'),
    path('dashboard/delete/<int:id>', DeleteReservationView.as_view(), name="delete-reservation"),
    path('dashboard/edit/<int:id>', EditReservationView.as_view(), name="edit"),
    path('dashboard/reservation/<int:id>', ReservationDetailView.as_view(), name="reservation-detail"),
    path('dashboard/metrics/', MetricTemplateView.as_view(), name="metrics"),
    path('addcustomer/', CreateReservationView.as_view(), name="addcustomer"),
    path('avaliable/', getAvaliability, name="avaliable"),
]