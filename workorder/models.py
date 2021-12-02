from django.db import models
from sites.models import Site
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User


class WorkorderQuerySet(models.QuerySet):
    def total_maintaince_cost_for_year(self, year):
        return self.filter(completed_at__year=year).aggregate(Sum('cost'))

class WorkOrder(models.Model):
    PRIORITIES = (
        (0, 'Low'),
        (1, 'Normal'),
        (2, 'High'),
    )
    title = models.CharField(max_length=255)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, related_name="workorders")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="managers")
    created_at = models.DateTimeField(default=timezone.now())
    completed_at = models.DateTimeField(null=True)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    priority = models.SmallIntegerField(default=0, choices=PRIORITIES)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    objects = WorkorderQuerySet.as_manager()

    def __str__(self):
        return f"{self.site}: {self.title}"
