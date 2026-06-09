from django.urls import path
from .views import (
    DashboardHomeView,
    DashboardLoginView,
)

urlpatterns = [
    path('', DashboardLoginView.as_view(), name="loginuser"),
    path('dashboard/', DashboardHomeView.as_view(), name='home'),
]