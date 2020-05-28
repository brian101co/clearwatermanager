from django.shortcuts import render, redirect
from .models import Customer
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login, authenticate

def index(request):
    if request.user.is_authenticated:
        customers = Customer.objects.all()
        return render(request, 'manager/index.html', {"customers":customers})
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
            return render(request, 'manager/login.html', {'error':'Incorrect username or password'})
        else:
            login(request, user)
            return redirect('home')

def delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            customer = Customer.objects.get(pk=id)
            customer.delete()
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
                customer = Customer(name=name, site=lot, title=name, start=start, end=end, phoneNum=phoneNum)
                customer.save()
                return redirect('home')
            else:
                messages.error(request, 'Please make sure to fill out all the feilds.')
                return redirect('home')
    else:
        return redirect('loginuser')

def event(request):
    if request.user.is_authenticated:
        events = Customer.objects.all().values('id', 'category', 'title', 'start', 'end') 
        events_list = list(events) 
        return JsonResponse(events_list, safe=False)
    else:
        return redirect('loginuser')
