import pytz

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
from .helpers import ( 
    is_double_booked
)


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
    

class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    context_object_name = "reservations"
    template_name = "reservations/list_reservations.html"

    def get_queryset(self):
        today = timezone.now()
        queryset = Reservation.objects.all().order_by('start')
        filter_by = self.request.GET.get('filter')
        search = self.request.GET.get('q', '')

        if filter_by == 'active':
            queryset = queryset.filter(start__lte=today, end__gte=today, confirmed_checkout=False)
        elif filter_by == 'upcoming':
            queryset = queryset.filter(start__gt=today, confirmed_checkout=False)
        elif filter_by == 'longterm':
            queryset = queryset.filter(is_long_term=True, confirmed_checkout=False)
        elif filter_by == 'checkedout':
            queryset = queryset.filter(confirmed_checkout=True)

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
        context["payment"] = Payment.objects.filter(
            customer=self.object
        ).first()

        # Site Amenities
        site = Site.objects.filter(identifier=self.object.site).first()
        context["site"] = site

        # Estimated total
        if site and site.nightly_rate:
            monthly = duration.days // 30
            remaining_after_months = duration.days % 30
            weekly = remaining_after_months // 7
            remaining_days = remaining_after_months % 7

            estimated_total = Decimal('0')

            if site.monthly_rate and monthly:
                estimated_total += site.monthly_rate * monthly
            if site.weekly_rate and weekly:
                estimated_total += site.weekly_rate * weekly
            if remaining_days:
                estimated_total += site.nightly_rate * remaining_days

            # Fallback if no monthly/weekly rates set
            if estimated_total == 0:
                estimated_total = site.nightly_rate * duration.days

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
        created, metric = Metric.objects.get_or_create(customer=self.object)
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
        all_reservations = Reservation.objects.exclude(pk=self.kwargs["id"]).filter(site=site, confirmed_checkout=False,)
        if not is_double_booked(all_reservations, start.isoformat(), end.isoformat()):
            self.object = form.save()
            created, metric = Metric.objects.get_or_create(customer=self.object)
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
        all_reservations = Reservation.objects.filter(site=site, confirmed_checkout=False,)
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
    
    sites = list(Site.objects.filter(under_maintenance=False).values_list("identifier", flat=True))

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

    for reservation in Reservation.objects.filter(confirmed_checkout=False).all():
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