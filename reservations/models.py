from django.db import models
from django.utils import timezone

class ReservationQuerySet(models.QuerySet):
    def active(self):
        return self.filter(confirmed_checkout=False)

    def short_term(self):
        return self.filter(is_long_term=False)

    def long_term(self):
        return self.filter(is_long_term=True)

    def get_by_site(self, site):
        return self.filter(site=site)

    def checking_out_on(self, date):
        return self.short_term().filter(checkout__date=date)

    def checking_in_on(self, date):
        return self.short_term().filter(checkin__date=date)

    def overdue(self, date):
        return self.short_term().filter(checkout__date__lt=date)

    def expiring_leases_on(self, date):
        return self.long_term().filter(checkout__date=date)

    def overdue_leases_on(self, date):
        return self.long_term().filter(checkout__date__lt=date)

    def checked_out(self):
        return self.filter(confirmed_checkout=True)

    def upcoming(self):
        today = timezone.now().date()
        return self.filter(checkin__date__gt=today)
    
    def overlapping(self, checkin, checkout):
        return self.filter(checkin__lt=checkout, checkout__gt=checkin)

    def occupied_on(self, date):
        return self.filter(
            checkin__date__lte=date,
            checkout__date__gte=date,
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
    checkin = models.DateTimeField()
    checkout = models.DateTimeField()
    phone_num = models.CharField(max_length=25)
    info = models.TextField(blank=True)
    is_long_term = models.BooleanField(default=False)
    confirmed_checkout = models.BooleanField(default=False)

    def __str__(self):
        return self.name