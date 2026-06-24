import json

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from .models import Site
from reservations.models import Reservation
from .forms import SiteForm
from workorder.models import WorkOrder
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView, 
    DeleteView, 
    CreateView,
    UpdateView,
    ListView
)


class SiteListView(LoginRequiredMixin, ListView):
    model = Site
    context_object_name = "sites"
    template_name = "sites/list_sites.html"

    def get_queryset(self):
        return Site.objects.active().order_by("lot_id")


class SiteDetailView(LoginRequiredMixin, DetailView):
    model = Site
    pk_url_kwarg = "id"
    context_object_name = "site"
    template_name = "sites/site_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workorders"] = self.object.workorders.active()
        return context


class RetireSiteView(LoginRequiredMixin, DeleteView):
    model = Site
    pk_url_kwarg = "id"
    success_url = reverse_lazy('home')
    template_name = "sites/retire_site.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workorders"] = self.object.workorders.active()
        context["active_reservations"] = Reservation.objects.active().current_and_upcoming()
        return context

    def delete(self, request, *args, **kwargs):
        site = self.get_object()
        site.retired = True
        site.save()
        messages.success(request, f'Site {site.lot_id} has been retired.')
        return redirect(self.get_success_url())


class EditSiteView(LoginRequiredMixin, UpdateView):
    model = Site
    form_class = SiteForm
    pk_url_kwarg = "id"
    success_url = reverse_lazy('home')
    template_name = "sites/edit_site.html"

    def form_valid(self, form):
        messages.success(self.request, f'Site {form.instance.lot_id} has been updated.')
        return super().form_valid(form)


class CreateSiteView(LoginRequiredMixin, CreateView):
    form_class = SiteForm
    success_url = reverse_lazy("home")
    template_name = "sites/create_site.html"

    def form_valid(self, form):
        messages.success(self.request, f'Site {form.instance.lot_id} has been created.')
        return super().form_valid(form)


@login_required
def api_site_by_lot_id(request, lot_id):
    if request.method == "GET":
        site = get_object_or_404(Site.objects.active(), lot_id=lot_id)
        data = serializers.serialize("json", [site])
        return HttpResponse(data, content_type="application/json")

    elif request.method == "PUT":
        site = get_object_or_404(Site, lot_id=lot_id)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=400)
        site.info = data.get("info", site.info)
        site.save()
        data = serializers.serialize("json", [site])
        return HttpResponse(data, content_type="application/json", status=200)

    return HttpResponse(status=405)
