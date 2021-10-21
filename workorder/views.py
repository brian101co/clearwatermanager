from django.shortcuts import redirect, render
from .models import WorkOrder
from .forms import WorkorderForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,
    DeleteView,
    CreateView,
    UpdateView,
    ListView
)

def workorder_completed_view(request, id):
    workorder = WorkOrder.objects.get(pk=id)
    workorder.completed = True
    workorder.save()
    return redirect('workorder-list')

class WorkorderUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkOrder
    form_class = WorkorderForm
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('workorder-list')
    template_name = "workorders/edit_workorder.html"

class WorkorderDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkOrder
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('workorder-list')

class WorkorderListView(LoginRequiredMixin, ListView):
    context_object_name = "workorders"
    queryset = WorkOrder.objects.filter(completed=False)
    ordering = "created_at"
    template_name = "workorders/list_workorders.html"

class CompletedWorkorderListView(LoginRequiredMixin, ListView):
    context_object_name = "workorders"
    queryset = WorkOrder.objects.filter(completed=True)
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

class CompletedWorkorderDetailView(LoginRequiredMixin, DetailView):
    queryset = WorkOrder.objects.filter(completed=True)
    pk_url_kwarg = 'id'
    template_name= "workorders/workorder_detail.html"
