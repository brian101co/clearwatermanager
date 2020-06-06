from django.shortcuts import render, redirect
from manager.models import Customer
from django.http import JsonResponse
from datetime import date, timedelta

def getTotalReservations(request):
    if request.user.is_authenticated:
        reservations = Customer.objects.all().count()
        return JsonResponse(reservations, safe=False)
    else:
        return redirect('loginuser')

def getReservation(request, id):
    if request.user.is_authenticated:
        reservation = Customer.objects.filter(pk=id).all().values('id', 'title', 'start', 'end', 'site', 'phoneNum')
        resList = list(reservation)
        return JsonResponse(resList, safe=False)
    else:
        return redirect('loginuser')

def event(request):
    if request.user.is_authenticated:
        events = Customer.objects.all().values('id', 'title', 'start', 'end', 'site', 'phoneNum')
        events_list = list(events)
        return JsonResponse(events_list, safe=False)
    else:
        return redirect('loginuser')

def getNotifications(request):
    if request.user.is_authenticated:
        today = date.today()
        tomorrow = today + timedelta(days = 2) 
        notifications = Customer.objects.filter(end__range=[today, tomorrow]).all().values('title', 'end', 'site')
        notification_list = list(notifications)
        return JsonResponse(notification_list, safe=False)
    else:
        return redirect('loginuser')