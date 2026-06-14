from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import WorkOrder
from .forms import WorkorderForm
from django.contrib import messages
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

@login_required
def workorder_completed_view(request, id):
    workorder = get_object_or_404(WorkOrder, pk=id)
    workorder.completed = True
    workorder.completed_at = timezone.now()
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
    template_name = "workorders/delete_workorder.html"

    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Workorder "{self.get_object().title}" has been deleted.')
        return super().delete(request, *args, **kwargs)

class WorkorderListView(LoginRequiredMixin, ListView):
    context_object_name = "workorders"
    template_name = "workorders/list_workorders.html"

    def get_queryset(self):
        site = self.request.GET.get("site", None)
        if site:
            return WorkOrder.objects.active().get_by_site(site).order_by("-priority")
        return WorkOrder.objects.active().order_by("-priority")

class CompletedWorkorderListView(LoginRequiredMixin, ListView):
    context_object_name = "workorders"
    queryset = WorkOrder.objects.completed_orders()
    ordering = "created_at"
    template_name = "workorders/completed_workorders.html"

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
