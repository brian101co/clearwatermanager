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
    template_name = "manager/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now()
        tomorrow = today + timedelta(days=1)
        thirty_days = today + timedelta(days=30)

        # Search query
        search = self.request.GET.get('q', '')

        customers = Reservation.objects.filter(
            end__gte=today,
            confirmed_checkout=False,
        ).order_by('start')

        # Apply search filter
        if search:
            customers = customers.filter(
                Q(name__icontains=search) |
                Q(site__icontains=search) |
                Q(phoneNum__icontains=search)
            )

        context["search"] = search
        context["customers"] = customers.filter(is_long_term=False)
        context["longterms"] = customers.filter(is_long_term=True)
        context["totalReservations"] = customers.count()
        context["checking_out_soon"] = customers.filter(end__date=tomorrow.date(), is_long_term=False)
        context["checking_in_soon"] = customers.filter(start__date=tomorrow.date(), is_long_term=False)
        context["expiring_leases"] = customers.filter(end__date__lte=thirty_days.date(), is_long_term=True)

        # Calculating Occupancy Rate
        total_lots = 65
        occupied_lots = Reservation.objects.filter(start__date__lte=today, end__date__gte=today).values("site", "name", "end")
        occupied_today = Reservation.objects.filter(start__date__lte=today, end__date__gte=today).count()
        occupancy_rate = round((occupied_today / total_lots) * 100)
        context["occupancy_rate"] = occupancy_rate
        context["occupied_lots"] = json.dumps(list(occupied_lots), cls=DjangoJSONEncoder)

        context["unpaid_payments"] = Payment.objects.filter(
            status__in=['unpaid', 'partial']
        ).count()

        context["checking_out_today"] = Reservation.objects.filter(
            end__date=today.date(),
            is_long_term=False,
            confirmed_checkout=False,
        )

        context["overdue_checkouts"] = Reservation.objects.filter(
            end__lt=today.date(),
            is_long_term=False,
            confirmed_checkout=False,
        )

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class DashboardLoginView(LoginView):
    template_name = "manager/dashboard_login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')