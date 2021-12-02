import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Site
from workorder.models import WorkOrder

def get_site_info(request, site):
    if request.method == "POST":
        data = json.load(request)
        site, created = Site.objects.get_or_create(identifier=site)
        site.info = data["info"]
        site.save()
        return JsonResponse({"updated": True})

    site_info = Site.objects.filter(identifier=site).values()
    total_workorders = WorkOrder.objects.filter(site__identifier=site, completed=False).count()
    if site_info:
        data_dict = {
            "site_info": list(site_info),
            "workorders": total_workorders
        }
        data = json.dumps([data_dict])
        return HttpResponse(data, content_type="application/json")
    return HttpResponse(status=404)
