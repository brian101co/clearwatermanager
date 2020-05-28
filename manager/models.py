from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    site = models.IntegerField(null=True)
    category = models.CharField(default='time', max_length=10)
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    phoneNum = models.CharField(max_length=25)

    def __str__(self):
        return self.name