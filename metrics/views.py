from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView, 
    DeleteView, 
    TemplateView, 
    CreateView,
    UpdateView
)
from django.contrib import messages
from .models import Metric
from workorder.models import WorkOrder
from datetime import datetime


class MetricTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "metrics/metrics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = datetime.now().year
        
        # Get the year of the first ever reservation
        first_metric = Metric.objects.order_by('start').first()
        start_year = first_metric.start.year if first_metric else current_year
        
        # Generate list from current year back to first reservation year
        context["available_years"] = list(range(current_year, start_year - 1, -1))
        context["current_year"] = current_year
        return context


@login_required
def metrics(request):
    year = request.GET.get("year")

    # Validate year
    if year:
        try:
            year = int(year)
        except ValueError:
            return JsonResponse({'error': 'Invalid year'}, status=400)
        
    # Reservations per month
    if request.GET.get("reservations"):
        if not year:
            return JsonResponse({'error': 'Year required'}, status=400)
        return JsonResponse(
            Metric.objects.reservations_per_month(year), 
            safe=False
        )
    
    # Cancellation rate
    elif request.GET.get("cancellation_rate"):
        if not year:
            return JsonResponse({'error': 'Year required'}, status=400)
        return JsonResponse(
            {'rate': Metric.objects.cancellation_rate(year)}
        )
    
    # Cancellations per month
    elif request.GET.get("cancellations"):
        if not year:
            return JsonResponse({'error': 'Year required'}, status=400)
        return JsonResponse(
            Metric.objects.cancellations_per_month(year),
            safe=False
        )

    # Maintenance costs
    elif request.GET.get("maintenance_costs"):
        if not year:
            return JsonResponse({'error': 'Year required'}, status=400)
        return JsonResponse(
            WorkOrder.objects.total_maintaince_cost_for_year(year)
        )

    # Most popular sites
    elif request.GET.get("popular_sites"):
        return JsonResponse(
            list(Metric.objects.most_popular_sites()),
            safe=False
        )

    # Reservations per year (all years)
    elif request.GET.get("per_year"):
        return JsonResponse(
            list(Metric.objects.reservations_per_year()),
            safe=False
        )
    
    elif request.GET.get("comparison"):
        if not year:
            return JsonResponse({'error': 'Year required'}, status=400)
        current = Metric.objects.reservations_per_month(year)
        previous = Metric.objects.reservations_per_month(year - 1)
        current_total = sum(r['total'] for r in current)
        previous_total = sum(r['total'] for r in previous)
        
        if previous_total > 0:
            trend = round(((current_total - previous_total) / previous_total) * 100)
        else:
            trend = 0
        
        return JsonResponse({
            'current_total': current_total,
            'previous_total': previous_total,
            'trend': trend
        })
    
    elif request.GET.get("reservation_types"):
        return JsonResponse(
            Metric.objects.reservations_by_type(),
            safe=False
        )

    # Fallback
    else:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)
    

