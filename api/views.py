from django.shortcuts import redirect
from manager.models import Customer, Metric
from workorder.models import WorkOrder
from django.http import JsonResponse
from datetime import date, timedelta

def getReservations(request):
    if request.user.is_authenticated:
        reservations = Customer.objects.all().values('id', 'name', 'start', 'end', 'site', 'phoneNum')
        resList = list(reservations)
        return JsonResponse(resList, safe=False)
    return redirect('loginuser')

def getReservation(request, id):
    if request.user.is_authenticated:
        reservation = Customer.objects.filter(pk=id).all().values('id', 'name', 'start', 'end', 'site', 'phoneNum', 'info')
        resList = list(reservation)
        return JsonResponse(resList, safe=False)
    return redirect('loginuser')

def metrics(request):
    if request.user.is_authenticated:
        if request.GET.get("last_month"):
            return JsonResponse(Metric.objects.last_month(), safe=False)
        elif request.GET.get("current_month"):
            return JsonResponse(Metric.objects.current_month(), safe=False)
        elif request.GET.get("cancelations"):
            return JsonResponse(Metric.objects.cancelations_per_month(int(request.GET.get("year"))), safe=False)
        elif request.GET.get("maintenace_costs"):
            return JsonResponse(WorkOrder.objects.total_maintaince_cost_for_year(int(request.GET.get("year"))))
        elif request.GET.get("year"):
            return JsonResponse(Metric.objects.reservations_per_month(int(request.GET.get("year"))), safe=False)
        else:
            metrics = Metric.objects.all().values()
            data = list(metrics)
            return JsonResponse(data, safe=False)

def getNotifications(request):
    if request.user.is_authenticated:
        today = date.today()
        tomorrow = today + timedelta(days = 2)
        notifications = Customer.objects.filter(end__range=[today, tomorrow]).all().values('name', 'end', 'site')
        notification_list = list(notifications)
        return JsonResponse(notification_list, safe=False)
    return redirect('loginuser')
