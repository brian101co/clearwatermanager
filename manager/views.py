import pytz

from django.shortcuts import render, redirect
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
from .models import Customer, Metric
from django.contrib import messages
from datetime import date, datetime, timedelta
from .helpers import ( 
    is_double_booked
)


class MetricTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "metrics/metrics.html"

class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = "manager/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now()
        tomorrow = today + timedelta(days=1)
        customers = Customer.objects.filter(end__gte=today).order_by('start')
        context["reservation_form"] = ReservationForm()
        context["customers"] = customers.filter(is_long_term=False)
        context["longterms"] = customers.filter(is_long_term=True)
        context["totalReservations"] = customers.count()
        context["checking_out_soon"] = customers.filter(end__date=tomorrow.date(), is_long_term=False)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        today = date.today()
        checkedout = Customer.objects.filter(end__lt=today).all()
        checkedout.delete()
        return self.render_to_response(context)

class DashboardLoginView(LoginView):
    template_name = "manager/dashboard_login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    pk_url_kwarg = "id"
    context_object_name = "reservation"
    template_name = "manager/reservation_detail.html"

class DeleteReservationView(LoginRequiredMixin, DeleteView):
    model = Customer
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
    model = Customer
    form_class = ReservationForm
    pk_url_kwarg = "id"
    success_url = reverse_lazy('home')
    template_name = "manager/edit_reservation.html"

    def form_valid(self, form):
        site = form.cleaned_data["site"]
        start = form.cleaned_data["start"]
        end = form.cleaned_data["end"]
        all_reservations = Customer.objects.exclude(pk=self.kwargs["id"]).filter(site=site)
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
        all_reservations = Customer.objects.filter(site=site)
        if not is_double_booked(all_reservations, start.isoformat(), end.isoformat()):
            self.object = form.save()
            metric = Metric(site=site, start=start, end=end, customer=self.object)
            metric.save()
            return HttpResponseRedirect(self.get_success_url())
        messages.error(self.request, 'Unavaliable.')
        return redirect('home')
    

def getAvailability(request):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    
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

    for reservation in Customer.objects.all():
        start = reservation.start.replace(tzinfo=pytz.UTC)
        end = reservation.end.replace(tzinfo=pytz.UTC)
        if checkin < end and checkout > start:  
            try:
                sites.remove(reservation.site.strip())
            except ValueError:
                pass  # site already removed or not in list

    context = {
        "reservation_form": ReservationForm(),
        "sites": sites,
        "checkin": checkin,
        "checkout": checkout,
        "start": checkin_str,
        "end": checkout_str,
    }
    return render(request, "manager/available_sites.html", context=context)
