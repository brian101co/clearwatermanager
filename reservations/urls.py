from django.urls import path
from .views import (
    checkout_reservation,
    ReservationDetailView,
    DeleteReservationView,
    CreateReservationView,
    EditReservationView,
    getAvailability
)

urlpatterns = [
    path('new', CreateReservationView.as_view(), name="addcustomer"),
    path('<int:id>/delete', DeleteReservationView.as_view(), name="delete-reservation"),
    path('<int:id>/edit', EditReservationView.as_view(), name="edit"),
    path('<int:id>/checkout', checkout_reservation, name="reservation-checkout"),
    path('<int:id>', ReservationDetailView.as_view(), name="reservation-detail"),
    path('avaliable/', getAvailability, name="avaliable"),
]