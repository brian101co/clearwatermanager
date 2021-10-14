import pytz, json

from django.shortcuts import render, redirect
from .models import Customer, Metric
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from dateutil import parser
from django.utils import timezone
from datetime import date, datetime
from .utils import get_short_term_reservations, get_long_term_reservations


def index(request):
    if request.user.is_authenticated:
        today = date.today()
        checkedout = Customer.objects.filter(end__lt=today).all()
        checkedout.delete()

        customers = Customer.objects.all().order_by('start')

        long_terms = get_long_term_reservations(customers)
        short_terms = get_short_term_reservations(customers)

        reservations = Customer.objects.all().count()

        return render(request, 'manager/index.html',
                      {
                          "customers": short_terms,
                          "totalReservations": reservations,
                          "longterms": long_terms,
                      })
    else:
        return redirect('loginuser')

def reservation_detail(request, id):
    reservation = Customer.objects.get(pk=id)
    return render(request, 'manager/reservation_detail.html', {"reservation": reservation})

def loginuser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'GET':
            return render(request, 'manager/login.html')
        else:
            user = authenticate(
                request, username=request.POST['login'], password=request.POST['password'])
            if user is None:
                return render(request, 'manager/login.html', {'error': 'Incorrect username or password'})
            else:
                login(request, user)
                # return render(request, 'manager/index.html')
                return redirect('home')

def delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            customer = Customer.objects.get(pk=id)
            metric = Metric.objects.get(customer=customer)
            metric.canceled = True
            metric.save()
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
            info = request.POST.get('info')

            reservation = Customer.objects.get(pk=id)

            reservation.name = name
            reservation.site = lot
            reservation.start = start
            reservation.end = end
            reservation.phoneNum = phoneNum
            reservation.info = info

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
            info = request.POST.get('info')

            if name and start and end and lot and phoneNum:
                try:
                    res = Customer.objects.get(site=lot)
                    if parser.parse(start) < timezone.make_naive(res.start, timezone=None) or parser.parse(start) > timezone.make_naive(res.end, timezone=None):
                        if parser.parse(end) < timezone.make_naive(res.start, timezone=None) or parser.parse(end) > timezone.make_naive(res.end, timezone=None):
                            customer = Customer(name=name, site=lot, start=start, end=end, phoneNum=phoneNum, info=info)
                            metric = Metric(site=lot, start=start, end=end, customer=customer)
                            customer.save()
                            metric.save()
                            return redirect('home')
                        else:
                            messages.error(request, 'Unavaliable.')
                            return redirect('home')
                    else:
                        messages.error(request, 'Unavaliable.')
                        return redirect('home')
                except ObjectDoesNotExist:
                    customer = Customer(name=name, site=lot, start=start, end=end, phoneNum=phoneNum, info=info)
                    metric = Metric(site=lot, start=start, end=end, customer=customer)
                    metric.save()
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
                        customer = Customer(
                            name=name, site=lot, start=start, end=end, phoneNum=phoneNum, info=info)
                        metric = Metric(site=lot, start=start, end=end, customer=customer)
                        metric.save()
                        customer.save()
                        return redirect('home')
            else:
                messages.error(
                    request, 'Please make sure to fill out all the feilds.')
                return redirect('home')
    else:
        return redirect('loginuser')


def getAvaliability(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            sites = ["122", "120", "118", "116", "114", "112", "110", "108", "106", "104", "102", "19", "17", "15", "13", "11",
                     "9", "7", "5", "6", "8", "10", "12", "14", "10C", "12C", "14C", "16", "18", "20", "22", "24", "26", "28",
                     "30", "85", "51", "53", "55", "57", "59", "65", "67", "69", "73", "75", "77", "79", "81", "83", "82", "80",
                     "78", "76", "74", "72", "70", "68", "66", "64", "62", "60", "58", "56", "63"]
            checkin = datetime.fromisoformat(request.POST.get('checkin')).replace(tzinfo=pytz.UTC)
            checkout = datetime.fromisoformat(request.POST.get('checkout')).replace(tzinfo=pytz.UTC)

            try:
                all_reservations = Customer.objects.all()
                for reservation in all_reservations:
                    end = reservation.end.replace(tzinfo=pytz.UTC)
                    start = reservation.start.replace(tzinfo=pytz.UTC)
                    print(f'{reservation.site} Start: {start}, End: {end}')
                    if checkin >= start and checkin <= end:
                        # print(reservation.site)
                        try:
                            sites.remove(reservation.site.strip())
                        except Exception as e:
                            print(e)
                    elif checkin <= start and checkout > start:
                        # print(reservation.site)
                        try:
                            sites.remove(reservation.site.strip())
                        except Exception as e:
                            print(e)
            except ValueError as e:
                print(e)
            except Exception as e:
                print(e)
                return redirect('home')
            return render(request, "manager/openings.html", {"sites": sites, "checkin": checkin, "checkout": checkout})
    else:
        return redirect('loginuser')

def metric(request):  
    return render(request, "metrics/metrics.html")
