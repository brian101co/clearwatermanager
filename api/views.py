from django.shortcuts import redirect
from manager.models import Customer
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

def getNotifications(request):
    if request.user.is_authenticated:
        today = date.today()
        tomorrow = today + timedelta(days = 2)
        notifications = Customer.objects.filter(end__range=[today, tomorrow]).all().values('name', 'end', 'site')
        notification_list = list(notifications)
        return JsonResponse(notification_list, safe=False)
    return redirect('loginuser')
