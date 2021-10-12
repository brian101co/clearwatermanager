import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Site

def get_site_info(request, site):
    if request.method == "POST":
        data = json.load(request)
        site, created = Site.objects.get_or_create(identifier=site)
        site.info = data["info"]
        site.save()
        return JsonResponse({"updated": True})
    qs = Site.objects.filter(identifier=site).values()
    if qs:
        data = json.dumps(list(qs))
        return HttpResponse(data, content_type="application/json")
    return HttpResponse(status=404)
