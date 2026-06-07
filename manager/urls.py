from django.urls import path
from .views import (
    DashboardHomeView,
    DashboardLoginView,
    checkout_reservation,
    ReservationDetailView,
    DeleteReservationView,
    CreateReservationView,
    EditReservationView,
    getAvailability
)

urlpatterns = [
    path('', DashboardLoginView.as_view(), name="loginuser"),
    path('dashboard/', DashboardHomeView.as_view(), name='home'),
    path('reservation/new', CreateReservationView.as_view(), name="addcustomer"),
    path('reservation/<int:id>/delete', DeleteReservationView.as_view(), name="delete-reservation"),
    path('reservation/<int:id>/edit', EditReservationView.as_view(), name="edit"),
    path('reservation/<int:id>/checkout', checkout_reservation, name="reservation-checkout"),
    path('reservation/<int:id>', ReservationDetailView.as_view(), name="reservation-detail"),
    path('avaliable/', getAvailability, name="avaliable"),
]