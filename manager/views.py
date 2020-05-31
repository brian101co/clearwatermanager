from django.shortcuts import render, redirect
from .models import Customer
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from dateutil import parser
from django.utils import timezone


def index(request):
    if request.user.is_authenticated:
        customers = Customer.objects.all()
        return render(request, 'manager/index.html', {"customers": customers})
    else:
        return redirect('loginuser')


def calendar(request):
    if request.user.is_authenticated:
        return render(request, 'manager/calendar.html')
    else:
        return redirect('loginuser')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'manager/login.html')
    else:
        user = authenticate(request, username=request.POST['login'], password=request.POST['password'])
        if user is None:
            return render(request, 'manager/login.html', {'error': 'Incorrect username or password'})
        else:
            login(request, user)
            return render(request, 'manager/index.html')


def delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            customer = Customer.objects.get(pk=id)
            customer.delete()
            return redirect('home')
    else:
        return redirect('loginuser')

def edit(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name')
            start = request.POST.get('checkin')
            end = request.POST.get('checkout')
            lot = request.POST.get('lot')
            phoneNum = request.POST.get('phone')

            reservation = Customer.objects.get(pk=id)
            
            reservation.name = name
            reservation.title = name
            reservation.site = lot
            reservation.start = start
            reservation.end = end
            reservation.phoneNum = phoneNum

            reservation.save()
            return redirect('home')
    else:
        return redirect('loginuser')


def addCustomer(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name')
            start = request.POST.get('checkin')
            end = request.POST.get('checkout')
            lot = request.POST.get('lot')
            phoneNum = request.POST.get('phone')

            if name and start and end and lot and phoneNum:
                try:
                    res = Customer.objects.get(site=lot)
                    if parser.parse(start) < timezone.make_naive(res.start, timezone=None) or parser.parse(start) > timezone.make_naive(res.end, timezone=None):
                        if parser.parse(end) < timezone.make_naive(res.start, timezone=None) or parser.parse(end) > timezone.make_naive(res.end, timezone=None):
                            customer = Customer(name=name, site=lot, title=name, start=start, end=end, phoneNum=phoneNum)
                            customer.save()
                            return redirect('home')
                        else:
                            messages.error(request, 'Unavaliable.')
                            return redirect('home')
                    else:
                        messages.error(request, 'Unavaliable.')
                        return redirect('home')
                except ObjectDoesNotExist:
                    customer = Customer(name=name, site=lot, title=name, start=start, end=end, phoneNum=phoneNum)
                    customer.save()
                    return redirect('home')
                except MultipleObjectsReturned:
                    reservations = Customer.objects.filter(site=lot).all()
                    reservationList = list(reservations)

                    overlap = False

                    for res in reservationList:
                        if parser.parse(start) < timezone.make_naive(res.start, timezone=None) or parser.parse(start) > timezone.make_naive(res.end, timezone=None):
                            if parser.parse(end) < timezone.make_naive(res.start, timezone=None) or parser.parse(end) > timezone.make_naive(res.end, timezone=None):
                                overlap = False
                            else:
                                overlap = True
                                break
                        else:
                            overlap = True
                            break

                    if overlap:
                        messages.error(request, 'Lot is Unavaliable.')
                        return redirect('home')
                    else:
                        customer = Customer(name=name, site=lot, title=name, start=start, end=end, phoneNum=phoneNum)
                        customer.save()
                        return redirect('home')
            else:
                messages.error(
                    request, 'Please make sure to fill out all the feilds.')
                return redirect('home')
    else:
        return redirect('loginuser')


def event(request):
    if request.user.is_authenticated:
        events = Customer.objects.all().values('id', 'title', 'start', 'end', 'site', 'phoneNum')
        events_list = list(events)
        return JsonResponse(events_list, safe=False)
    else:
        return redirect('loginuser')

def getReservation(request, id):
    if request.user.is_authenticated:
        reservation = Customer.objects.filter(pk=id).all().values('id', 'title', 'start', 'end', 'site', 'phoneNum')
        resList = list(reservation)
        return JsonResponse(resList, safe=False)
    else:
        return redirect('loginuser')


def getAvaliability(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            lot = request.POST.get('lot')
            start = request.POST.get('checkin')
            end = request.POST.get('checkout')
            try:
                res = Customer.objects.get(site=lot)
                if parser.parse(start) < timezone.make_naive(res.start, timezone=None) or parser.parse(start) > timezone.make_naive(res.end, timezone=None):
                    if parser.parse(end) < timezone.make_naive(res.start, timezone=None) or parser.parse(end) > timezone.make_naive(res.end, timezone=None):
                        messages.success(request, 'Avaliable.')
                        return redirect('home')
                    else:
                        messages.error(request, 'Unavaliable.')
                        return redirect('home')
                else:
                    messages.error(request, 'Unavaliable.')
                    return redirect('home')
            except ObjectDoesNotExist:
                messages.success(request, 'Avaliable.')
                return redirect('home')
            except MultipleObjectsReturned:
                reservations = Customer.objects.filter(site=lot).all()
                reservationList = list(reservations)
                overlap = False

                for res in reservationList:
                    if parser.parse(start) < timezone.make_naive(res.start, timezone=None) or parser.parse(start) > timezone.make_naive(res.end, timezone=None):
                        if parser.parse(end) < timezone.make_naive(res.start, timezone=None) or parser.parse(end) > timezone.make_naive(res.end, timezone=None):
                            overlap = False
                        else:
                            overlap = True
                            break
                    else:
                        overlap = True
                        break

                if overlap:
                    messages.error(request, 'Unavaliable.')
                    return redirect('home')
                else:
                    messages.success(request, 'Avaliable.')
                    return redirect('home')
    else:
        return redirect('loginuser')
