import json

from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, 
)
from reservations.models import Reservation
from payments.models import Payment
from sites.models import Site
from datetime import timedelta


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        now = timezone.now()
        today = now.date()
        tomorrow = today + timedelta(days=1)

        reservations = Reservation.objects.active().order_by("checkin")
        occupied = Reservation.objects.occupied_on(today)

        context.update({
            "checking_out_today": reservations.checking_out_on(today),
            "checking_out_tomorrow": reservations.checking_out_on(tomorrow),
            "checking_in_tomorrow": reservations.checking_in_on(tomorrow),
            "expiring_leases": reservations.expiring_leases_on(today),
            "overdue_leases": reservations.overdue_leases_on(today),
            "overdue_checkouts": reservations.overdue(today),
            "occupancy_rate": round(occupied.count() / Site.objects.count() * 100),
            "occupied_lots": json.dumps(list(occupied.values("site", "name", "checkout")), cls=DjangoJSONEncoder),
            "unpaid_payments": Payment.objects.filter(
                status__in=["unpaid", "partial"]
            ).count(),
        })

        return context


class DashboardLoginView(LoginView):
    template_name = "dashboard/dashboard_login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')