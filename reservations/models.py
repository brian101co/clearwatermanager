from django.db import models
from django.utils import timezone

class ReservationQuerySet(models.QuerySet):
    def active(self):
        return self.filter(confirmed_checkout=False)

    def short_term(self):
        return self.filter(is_long_term=False)

    def long_term(self):
        return self.filter(is_long_term=True)

    def checking_out_on(self, date):
        return self.short_term().filter(end__date=date)

    def checking_in_on(self, date):
        return self.short_term().filter(start__date=date)

    def overdue(self, date):
        return self.short_term().filter(end__date__lt=date)

    def expiring_leases_on(self, date):
        return self.long_term().filter(end__date=date)

    def checked_out(self):
        return self.filter(confirmed_checkout=True)

    def upcoming(self):
        today = timezone.now().date()
        return self.filter(start__date__gt=today)

    def occupied_on(self, date):
        return self.filter(
            start__date__lte=date,
            end__date__gte=date,
            confirmed_checkout=False,
        )


class ReservationManager(models.Manager):
    def get_queryset(self):
        return ReservationQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()
    
    def occupied_on(self, date):
        return self.get_queryset().occupied_on(date)
    
    def checked_out(self):
        return self.get_queryset().checked_out()


class Reservation(models.Model):

    objects = ReservationManager()

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