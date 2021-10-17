import pytz

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
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
from datetime import date, datetime
from .helpers import (
    get_short_term_reservations, 
    get_long_term_reservations, 
    is_double_booked
)


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = "manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customers = Customer.objects.all().order_by('start')
        context["reservation_form"] = ReservationForm()
        context["customers"] = get_short_term_reservations(customers)
        context["longterms"] = get_long_term_reservations(customers)
        context["totalReservations"] = Customer.objects.all().count()
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
        messages.error(self.request, 'Unavaliable.')
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


def getAvaliability(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            sites = ["122", "120", "118", "116", "114", "112", "110", "108", "106", "104", "102", "19", "17", "15", "13", "11",
                     "9", "7", "5", "6", "8", "10", "12", "14", "10C", "12C", "14C", "16", "18", "20", "22", "24", "26", "28",
                     "30", "85", "51", "53", "55", "57", "59", "65", "67", "69", "73", "75", "77", "79", "81", "83", "82", "80",
                     "78", "76", "74", "72", "70", "68", "66", "64", "62", "60", "58", "56", "63"]
            checkin = datetime.fromisoformat(request.POST.get('checkin')).replace(tzinfo=pytz.UTC)
            checkout = datetime.fromisoformat(request.POST.get('checkout')).replace(tzinfo=pytz.UTC)

            try:
                all_reservations = Customer.objects.all()
                for reservation in all_reservations:
                    end = reservation.end.replace(tzinfo=pytz.UTC)
                    start = reservation.start.replace(tzinfo=pytz.UTC)
                    if checkin >= start and checkin <= end:
                        try:
                            sites.remove(reservation.site.strip())
                        except Exception as e:
                            print(e)
                    elif checkin <= start and checkout > start:
                        try:
                            sites.remove(reservation.site.strip())
                        except Exception as e:
                            print(e)
            except ValueError as e:
                print(e)
            except Exception as e:
                print(e)
                return redirect('home')
            return render(request, "manager/openings.html", {"sites": sites, "checkin": checkin, "checkout": checkout})
    else:
        return redirect('loginuser')

def metric(request):  
    return render(request, "metrics/metrics.html")
