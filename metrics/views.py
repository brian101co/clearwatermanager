from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView, 
    DeleteView, 
    TemplateView, 
    CreateView,
    UpdateView
)
from django.contrib import messages


class MetricTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "metrics/metrics.html"
