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

class Metric(models.Model):
    site = models.CharField(max_length=4)
    start = models.DateTimeField()
    end = models.DateTimeField()
    canceled = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.site