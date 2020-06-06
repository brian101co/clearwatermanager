from django.shortcuts import render, redirect
from manager.models import Customer
from django.http import JsonResponse

def getTotalReservations(request):
    if request.user.is_authenticated:
        reservations = Customer.objects.all().count()
        return JsonResponse(reservations, safe=False)
    else:
        return redirect('loginuser')
