import json

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import Site
from .forms import SiteForm
from workorder.models import WorkOrder
from django.urls import reverse_lazy
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
    ordering = ["identifier"]


class SiteDetailView(LoginRequiredMixin, DetailView):
    model = Site
    pk_url_kwarg = "id"
    context_object_name = "site"
    template_name = "sites/site_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workorders"] = self.object.workorders.active()
        return context


class DeleteSiteView(LoginRequiredMixin, DeleteView):
    model = Site
    pk_url_kwarg = "id"
    success_url = reverse_lazy('home')
    template_name = "sites/delete_site.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workorders"] = self.object.workorders.active()
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Site {self.get_object().identifier} has been deleted.')
        return super().delete(request, *args, **kwargs)


class EditSiteView(LoginRequiredMixin, UpdateView):
    model = Site
    form_class = SiteForm
    pk_url_kwarg = "id"
    success_url = reverse_lazy('home')
    template_name = "sites/edit_site.html"

    def form_valid(self, form):
        messages.success(self.request, f'Site {form.instance.identifier} has been updated.')
        return super().form_valid(form)


class CreateSiteView(LoginRequiredMixin, CreateView):
    form_class = SiteForm
    success_url = reverse_lazy("home")
    template_name = "sites/create_site.html"

    def form_valid(self, form):
        messages.success(self.request, f'Site {form.instance.identifier} has been created.')
        return super().form_valid(form)


@login_required
def get_site_info(request, site):
    if request.method == "POST":
        data = json.load(request)
        site, created = Site.objects.get_or_create(identifier=site)
        site.info = data["info"]
        site.save()
        return JsonResponse({
            "site": Site.objects.filter(pk=site.pk).values().first()
        })

    site_info = Site.objects.filter(identifier=site).values()

    if site_info:
        return JsonResponse({
            "site_info": list(site_info),
            "workorders": WorkOrder.objects.active().get_by_site(site).count()
        })
    
    return HttpResponse(status=404)
