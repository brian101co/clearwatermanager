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
from django.db.models import Q
from datetime import timedelta



class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now()
        tomorrow = today + timedelta(days=1)
        today_date = today.date()
        tomorrow_date = tomorrow.date()

        # Base queryset
        reservations = Reservation.objects.filter(
            confirmed_checkout=False
        ).order_by('start')

        context["totalReservations"] = reservations.count()
        context["checking_out_soon"] = reservations.filter(
            end__date=tomorrow_date,
            is_long_term=False
        )
        context["checking_in_soon"] = reservations.filter(
            start__date=tomorrow_date,
            is_long_term=False
        )
        context["expiring_leases"] = reservations.filter(
            end__date=today_date,
            is_long_term=True
        )
        context["checking_out_today"] = reservations.filter(
            end__date=today_date,
            is_long_term=False
        )
        context["overdue_checkouts"] = reservations.filter(
            end__date__lt=today_date,
            is_long_term=False
        )

        # Occupancy Rate
        total_lots = 65
        occupied_lots = Reservation.objects.filter(
            start__date__lte=today_date,
            end__date__gte=today_date,
            confirmed_checkout=False,
        ).values("site", "name", "end")

        context["occupancy_rate"] = round((occupied_lots.count() / total_lots) * 100)
        context["occupied_lots"] = json.dumps(list(occupied_lots), cls=DjangoJSONEncoder)
        context["unpaid_payments"] = Payment.objects.filter(
            status__in=['unpaid', 'partial']
        ).count()

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class DashboardLoginView(LoginView):
    template_name = "dashboard/dashboard_login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')