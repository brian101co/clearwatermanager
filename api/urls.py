from django.urls import path, include
from . import views

urlpatterns = [
    path('reservations/', views.getTotalReservations),
    path('reservation/<int:id>/', views.getReservation, name="reservation"),
    path('events/', views.event, name="events"),
    path('notifications/', views.getNotifications, name="notifications"),
]