from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.contrib.auth.decorators import login_required
from .models import Reservation


@login_required
def api_get_reservation_by_lot(request, lot_id):
    if request.method != "GET":
        return HttpResponse(status=405)
    data = serializers.serialize("json", Reservation.objects.active().get_by_site(lot_id))
    return HttpResponse(data, content_type="application/json")


@login_required
def api_get_reservations_on(request, date):
    if request.method != "GET":
        return HttpResponse(status=405)
    reservations = Reservation.objects.active().occupied_on(date).values(
        'name', 'checkin', 'checkout', 'phone_num', 'info', 'is_long_term', 'site__lot_id'
    )
    return JsonResponse(list(reservations), safe=False, encoder=DjangoJSONEncoder)
