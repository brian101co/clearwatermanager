from django.shortcuts import render
from .models import WorkOrder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,
    DeleteView,
    TemplateView,
    CreateView,
    UpdateView,
    ListView
)


class WorkOrderListView(LoginRequiredMixin, ListView):
    context_object_name = "workorders"
    model = WorkOrder
    ordering = "created_at"
    template_name = "workorders/list_workorders.html"
