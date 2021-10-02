import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Site

def get_site_info(request, site):
    qs = Site.objects.filter(identifier=site).values()
    if qs:
        data = json.dumps(list(qs))
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponse(status=404)
