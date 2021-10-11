from django.shortcuts import redirect
from manager.models import Customer
from django.http import JsonResponse
from datetime import date, timedelta
# from django.conf import settings
# from django.http import HttpResponse
# from twilio.rest import Client

def getTotalReservations(request):
    if request.user.is_authenticated:
        reservations = Customer.objects.all().count()
        return JsonResponse(reservations, safe=False)
    else:
        return redirect('loginuser')

def getReservation(request, id):
    if request.user.is_authenticated:
        reservation = Customer.objects.filter(pk=id).all().values('id', 'name', 'start', 'end', 'site', 'phoneNum')
        resList = list(reservation)
        return JsonResponse(resList, safe=False)
    else:
        return redirect('loginuser')

def event(request):
    if request.user.is_authenticated:
        events = Customer.objects.all().values('id', 'name', 'start', 'end', 'site', 'phoneNum')
        events_list = list(events)
        return JsonResponse(events_list, safe=False)
    else:
        return redirect('loginuser')

def getNotifications(request):
    if request.user.is_authenticated:
        today = date.today()
        tomorrow = today + timedelta(days = 2)
        notifications = Customer.objects.filter(end__range=[today, tomorrow]).all().values('name', 'end', 'site')
        notification_list = list(notifications)
        # for notification in notification_list:
        #     if notification:
        #         message_to_broadcast = f"{ notification['title'] } is checking out on { notification['end'].strftime('%m/%d/%Y') }. Site No: { notification['site'] }"
        #         client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        #         for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
        #             if recipient:
        #                 client.messages.create(to=recipient,
        #                                     from_=settings.TWILIO_NUMBER,
        #                                     body=message_to_broadcast)

        return JsonResponse(notification_list, safe=False)
    else:
        return redirect('loginuser')