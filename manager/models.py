import json

from datetime import datetime
from django.db import models
from django.db.models.deletion import SET_NULL

class Customer(models.Model):
    name = models.CharField(max_length=255)
    site = models.CharField(max_length=4)
    start = models.DateTimeField()
    end = models.DateTimeField()
    phoneNum = models.CharField(max_length=25)
    info = models.TextField(blank=True)

    def __str__(self):
        return self.name


class MetricQuerySet(models.QuerySet):
    def reservations_per_month(self, year):
        data = []
        for i in range(13):
            total_res_per_month = self.filter(start__year=year, start__month=i).count()
            if i == 1:
                data.append({"month": "Jan", "total": total_res_per_month})
            elif i == 2:
                data.append({"month": "Feb", "total": total_res_per_month})
            elif i == 3: 
                data.append({"month": "Mar", "total": total_res_per_month})
            elif i == 4: 
                data.append({"month": "Apr", "total": total_res_per_month})
            elif i == 5: 
                data.append({"month": "May", "total": total_res_per_month})
            elif i == 6: 
                data.append({"month": "Jun", "total": total_res_per_month})
            elif i == 7: 
                data.append({"month": "Jul", "total": total_res_per_month})
            elif i == 8: 
                data.append({"month": "Aug", "total": total_res_per_month})
            elif i == 9: 
                data.append({"month": "Sep", "total": total_res_per_month})
            elif i == 10: 
                data.append({"month": "Oct", "total": total_res_per_month})
            elif i == 11: 
                data.append({"month": "Nov", "total": total_res_per_month})
            elif i == 12: 
                data.append({"month": "Dec", "total": total_res_per_month})
        return data

    def cancelations_per_month(self, year):
        data = []
        for i in range(13):
            total_canc_per_month = self.filter(start__year=year, start__month=i, canceled=True).count()
            if i == 1:
                data.append({"month": "Jan", "total": total_canc_per_month})
            elif i == 2:
                data.append({"month": "Feb", "total": total_canc_per_month})
            elif i == 3: 
                data.append({"month": "Mar", "total": total_canc_per_month})
            elif i == 4: 
                data.append({"month": "Apr", "total": total_canc_per_month})
            elif i == 5: 
                data.append({"month": "May", "total": total_canc_per_month})
            elif i == 6: 
                data.append({"month": "Jun", "total": total_canc_per_month})
            elif i == 7: 
                data.append({"month": "Jul", "total": total_canc_per_month})
            elif i == 8: 
                data.append({"month": "Aug", "total": total_canc_per_month})
            elif i == 9: 
                data.append({"month": "Sep", "total": total_canc_per_month})
            elif i == 10: 
                data.append({"month": "Oct", "total": total_canc_per_month})
            elif i == 11: 
                data.append({"month": "Nov", "total": total_canc_per_month})
            elif i == 12: 
                data.append({"month": "Dec", "total": total_canc_per_month})
        return data

class Metric(models.Model):
    site = models.CharField(max_length=4)
    start = models.DateTimeField()
    end = models.DateTimeField()
    canceled = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    objects = MetricQuerySet.as_manager()

    def __str__(self):
        return self.site
