from django.db import models

class Reservation(models.Model):
    name = models.CharField(max_length=255)
    site = models.CharField(max_length=4)
    start = models.DateTimeField()
    end = models.DateTimeField()
    phoneNum = models.CharField(max_length=25)
    info = models.TextField(blank=True)
    is_long_term = models.BooleanField(default=False)
    confirmed_checkout = models.BooleanField(default=False)

    def __str__(self):
        return self.name