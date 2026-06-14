import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import ReservationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView, 
    DeleteView, 
    CreateView,
    UpdateView,
    ListView
)
from .models import Reservation
from payments.models import Payment
from metrics.models import Metric
from sites.models import Site
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from decimal import Decimal
from django.db.models import Q


@login_required
def checkout_reservation(request, id):
    if request.method != "POST":
        return redirect('home')
    
    reservation = get_object_or_404(Reservation, id=id)
    reservation.confirmed_checkout = True
    reservation.save()
    messages.success(request, f'{reservation.name} checked out.')
    return redirect('home')


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    context_object_name = "reservations"
    template_name = "reservations/list_reservations.html"

    def get_queryset(self):
        queryset = Reservation.objects.active().order_by('start')
        filter_by = self.request.GET.get('filter')
        search = self.request.GET.get('q', '')

        if filter_by == 'upcoming':
            queryset = queryset.upcoming()
        elif filter_by == 'longterm':
            queryset = queryset.long_term()
        elif filter_by == 'checkedout':
            queryset = Reservation.objects.checked_out()
        elif filter_by == 'all':
            queryset = Reservation.objects.all().order_by('start')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(site__icontains=search) |
                Q(phoneNum__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q', '')
        return context


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    pk_url_kwarg = "id"
    context_object_name = "reservation"
    template_name = "reservations/reservation_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now()

        # Duration of stay
        duration = self.object.end - self.object.start
        context["duration_of_stay"] = duration.days

        # Days remaining
        if self.object.end > today:
            days_remaining = self.object.end - today
            context["days_remaining"] = days_remaining.days
        else:
            context["days_remaining"] = 0

        # Payment status
        context["payment"] = Payment.objects.by_customer(self.object).first()

        # Site Amenities
        site = Site.objects.by_lot(self.object.site).first()
        context["site"] = site

        # Estimated total
        if site and site.nightly_rate:
            estimated_total = site.calculate_estimated_total(duration.days)
            context["estimated_total"] = estimated_total
            context["estimated_total_with_sales_tax"] = round(estimated_total * Decimal('1.07'), 2)

        return context
    

class DeleteReservationView(LoginRequiredMixin, DeleteView):
    model = Reservation
    pk_url_kwarg = "id"
    success_url = reverse_lazy('home')
    template_name = "reservations/delete_reservation.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        metric, created = Metric.objects.get_or_create(customer=self.object)
        metric.canceled = True
        metric.save()
        return super().delete(request, *args, **kwargs)


class EditReservationView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    pk_url_kwarg = "id"
    success_url = reverse_lazy('home')
    template_name = "reservations/edit_reservation.html"

    def form_valid(self, form):
        site = form.cleaned_data["site"]
        start = form.cleaned_data["start"]
        end = form.cleaned_data["end"]

        if not Reservation.objects.active().get_by_site(site).exclude(pk=self.kwargs["id"]).overlapping(start, end).exists():
            self.object = form.save()
            metric, created = Metric.objects.get_or_create(customer=self.object)
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
    template_name = 'reservations/new_reservation.html'

    def form_valid(self, form):
        site = form.cleaned_data["site"]
        start = form.cleaned_data["start"]
        end = form.cleaned_data["end"]

        if not Reservation.objects.active().get_by_site(site).overlapping(start, end).exists():
            self.object = form.save()
            Metric.objects.create(site=site, start=start, end=end, customer=self.object)
            return HttpResponseRedirect(self.get_success_url())
        
        messages.error(self.request, 'Unavailable. That site is already booked for the selected dates.')
        return redirect('home')
    

@login_required
def get_availability(request):    
    if request.method != "POST":
        return redirect('home')

    checkin_str = request.POST.get('checkin')
    checkout_str = request.POST.get('checkout')

    if not checkin_str or not checkout_str:
        messages.error(request, 'Please provide both checkin and checkout dates.')
        return redirect('home')

    try:
        checkin = datetime.fromisoformat(checkin_str).replace(tzinfo=timezone.utc)
        checkout = datetime.fromisoformat(checkout_str).replace(tzinfo=timezone.utc)
    except ValueError:
        messages.error(request, 'Invalid date format.')
        return redirect('home')

    if checkout <= checkin:
        messages.error(request, 'Checkout must be after checkin.')
        return redirect('home')
    
    booked_sites = Reservation.objects.active().overlapping(checkin, checkout).values_list("site", flat=True)
    site_objects = Site.objects.operational().exclude(identifier__in=booked_sites).order_by("identifier")

    context = {
        "reservation_form": ReservationForm(),
        "sites": json.dumps(list(site_objects.values_list("identifier", flat=True))),
        "site_objects": site_objects,
        "checkin": checkin,
        "checkout": checkout,
        "start": checkin_str,
        "end": checkout_str,
    }
    return render(request, "reservations/available_sites.html", context=context)


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