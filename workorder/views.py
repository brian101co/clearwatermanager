from django.shortcuts import render
from .models import WorkOrder
from .forms import WorkorderForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,
    DeleteView,
    TemplateView,
    CreateView,
    UpdateView,
    ListView
)


class WorkorderListView(LoginRequiredMixin, ListView):
    context_object_name = "workorders"
    model = WorkOrder
    ordering = "created_at"
    template_name = "workorders/list_workorders.html"

class WorkorderCreateView(LoginRequiredMixin, CreateView):
    form_class = WorkorderForm
    success_url = reverse_lazy("workorder-list")
    template_name="workorders/create_workorder.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.manager = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class WorkorderDetailView(LoginRequiredMixin, DetailView):
    model = WorkOrder
    pk_url_kwarg = 'id'
    template_name= "workorders/workorder_detail.html"
