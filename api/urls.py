from django.urls import path
from . import views

urlpatterns = [
    path('reservations/', views.getReservations, name="reservations"),
    path('reservation/<int:id>/', views.getReservation, name="reservation"),
    path('notifications/', views.getNotifications, name="notifications"),
]