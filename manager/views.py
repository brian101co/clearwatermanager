import pytz
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from .forms import ReservationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView, 
    DeleteView, 
    TemplateView, 
    CreateView,
    UpdateView
)
from .models import Reservation
from metrics.models import Metric
from sites.models import Site
from payments.models import Payment
from django.contrib import messages
from django.db.models import Q
from datetime import date, datetime, timedelta
from .helpers import ( 
    is_double_booked
)


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
        context["reservation_form"] = ReservationForm()
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


@login_required
def checkout_reservation(request, id):
    if request.method != "POST":
        return redirect('home')
    
    reservation = get_object_or_404(Reservation, id=id)
    reservation.confirmed_checkout = True
    
    try:
        reservation.save()
        messages.success(request, f'{reservation.name} checked out.')
        return redirect('home')
    except Exception as e:
        messages.error(request, f'An error has occurred. Please try again.')
        print(e) 
        return redirect('home')


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    pk_url_kwarg = "id"
    context_object_name = "reservation"
    template_name = "manager/reservation_detail.html"


class DeleteReservationView(LoginRequiredMixin, DeleteView):
    model = Reservation
    pk_url_kwarg = "id"
    success_url = reverse_lazy('home')
    template_name = "manager/delete_reservation.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        metric = Metric.objects.get(customer=self.object)
        metric.canceled = True
        metric.save()
        return super().delete(request, *args, **kwargs)


class EditReservationView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    pk_url_kwarg = "id"
    success_url = reverse_lazy('home')
    template_name = "manager/edit_reservation.html"

    def form_valid(self, form):
        site = form.cleaned_data["site"]
        start = form.cleaned_data["start"]
        end = form.cleaned_data["end"]
        all_reservations = Reservation.objects.exclude(pk=self.kwargs["id"]).filter(site=site)
        if not is_double_booked(all_reservations, start.isoformat(), end.isoformat()):
            self.object = form.save()
            metric = Metric.objects.get(customer=self.object)
            metric.start = start
            metric.end = end
            metric.site = site
            metric.save()
            return HttpResponseRedirect(self.get_success_url())
        messages.error(self.request, 'Unavailable. That site is already booked for the selected dates.')
        return redirect('home')


class CreateReservationView(LoginRequiredMixin, CreateView):
    form_class = ReservationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        site = form.cleaned_data["site"]
        start = form.cleaned_data["start"]
        end = form.cleaned_data["end"]
        all_reservations = Reservation.objects.filter(site=site)
        if not is_double_booked(all_reservations, start.isoformat(), end.isoformat()):
            self.object = form.save()
            metric = Metric(site=site, start=start, end=end, customer=self.object)
            metric.save()
            return HttpResponseRedirect(self.get_success_url())
        messages.error(self.request, 'Unavaliable.')
        return redirect('home')
    

@login_required
def getAvailability(request):    
    if request.method != "POST":
        return redirect('home')

    sites = ["122", "120", "118", "116", "114", "112", "110", "108", "106", "104", "102", "19", "17", "15", "13", "11",
            "9", "7", "5", "6", "8", "10", "12", "14", "10C", "12C", "14C", "16", "18", "20", "22", "24", "26", "28",
            "30", "85", "51", "53", "55", "57", "59", "65", "67", "69", "73", "75", "77", "79", "81", "83", "82", "80",
            "78", "76", "74", "72", "70", "68", "66", "64", "62", "60", "58", "56", "63"]

    checkin_str = request.POST.get('checkin')
    checkout_str = request.POST.get('checkout')

    if not checkin_str or not checkout_str:
        messages.error(request, 'Please provide both checkin and checkout dates.')
        return redirect('home')

    try:
        checkin = datetime.fromisoformat(checkin_str).replace(tzinfo=pytz.UTC)
        checkout = datetime.fromisoformat(checkout_str).replace(tzinfo=pytz.UTC)
    except ValueError:
        messages.error(request, 'Invalid date format.')
        return redirect('home')

    if checkout <= checkin:
        messages.error(request, 'Checkout must be after checkin.')
        return redirect('home')

    for reservation in Reservation.objects.all():
        start = reservation.start.replace(tzinfo=pytz.UTC)
        end = reservation.end.replace(tzinfo=pytz.UTC)
        if checkin < end and checkout > start:  
            try:
                sites.remove(reservation.site.strip())
            except ValueError:
                pass  # site already removed or not in list
    
    site_objects = Site.objects.filter(
        identifier__in=sites
    ).order_by("identifier")

    context = {
        "reservation_form": ReservationForm(),
        "sites": sites,
        "site_objects": site_objects,
        "checkin": checkin,
        "checkout": checkout,
        "start": checkin_str,
        "end": checkout_str,
    }
    return render(request, "manager/available_sites.html", context=context)


def handler500(request):
    messages.error(request, 'Something went wrong. Please try again.')
    return redirect('home')


def handler404(request, exception):
    messages.error(request, 'Page not found.')
    return redirect('home')


def handler403(request, exception):
    messages.error(request, 'You do not have permission to access that page.')
    return redirect('home')


def handler400(request, exception):
    messages.error(request, 'Bad request. Please try again.')
    return redirect('home')