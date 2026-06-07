from django.db import models
from manager.models import Reservation

MONTHS = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

class MetricQuerySet(models.QuerySet):

    def reservations_per_month(self, year):
        return [
            {
                "month": MONTHS[i],
                "total": self.filter(start__year=year, start__month=i).count()
            }
            for i in range(1, 13)
        ]

    def cancellations_per_month(self, year):
        return [
            {
                "month": MONTHS[i],
                "total": self.filter(start__year=year, start__month=i, canceled=True).count()
            }
            for i in range(1, 13)
        ]

    def reservations_by_type(self):
        long_term = self.filter(customer__is_long_term=True).count()
        short_term = self.filter(customer__is_long_term=False).count()
        total = self.count()
        return {
            'long_term': long_term,
            'short_term': short_term,
            'total': total
        }

    def reservations_per_year(self):
        from django.db.models import Count
        return self.values('start__year').annotate(
            total=Count('id')
        ).order_by('start__year')

    def cancellation_rate(self, year):
        total = self.filter(start__year=year).count()
        canceled = self.filter(start__year=year, canceled=True).count()
        return round((canceled / total) * 100) if total > 0 else 0

    def most_popular_sites(self):
        from django.db.models import Count
        return self.values('site').annotate(
            total=Count('id')
        ).order_by('-total')[:10]

    def average_stay_length(self, year):
        from django.db.models import Avg, ExpressionWrapper, F, DurationField
        return self.filter(start__year=year).annotate(
            duration=ExpressionWrapper(
                F('end') - F('start'),
                output_field=DurationField()
            )
        ).aggregate(avg=Avg('duration'))
    

class Metric(models.Model):
    site = models.CharField(max_length=4)
    start = models.DateTimeField()
    end = models.DateTimeField()
    canceled = models.BooleanField(default=False)
    customer = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True)
    res_type = models.PositiveSmallIntegerField(choices=(
        (1, "Daily"),
        (2, "Weekly"),
        (3, "Monthly")
    ), default=1)

    objects = MetricQuerySet.as_manager()

    def __str__(self):
        return self.site
