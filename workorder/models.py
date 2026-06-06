from django.db import models
from sites.models import Site
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User
from datetime import timedelta


class WorkorderQuerySet(models.QuerySet):
    def total_maintaince_cost_for_year(self, year):
        return self.filter(completed_at__year=year).aggregate(Sum('cost'))
    
    def by_category(self, category):
        return self.filter(category=category)

    def high_priority(self):
        return self.filter(priority=2)

    def overdue(self):
        return self.filter(completed=False, created_at__lt=timezone.now() - timedelta(days=7))
    

class WorkOrder(models.Model):
    PRIORITIES = (
        (0, 'Low'),
        (1, 'Normal'),
        (2, 'High'),
    )
    CATEGORIES = (
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('landscaping', 'Landscaping'),
        ('cleaning', 'Cleaning'),
        ('structural', 'Structural'),
        ('appliance', 'Appliance'),
        ('general', 'General'),
    )
    title = models.CharField(max_length=255)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, related_name="workorders")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="managers")
    category = models.CharField(max_length=20, choices=CATEGORIES, default='general')
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    priority = models.SmallIntegerField(default=0, choices=PRIORITIES)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    estimated_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='workorders/static/images', blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    recurring_interval = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Recurring interval in days")

    objects = WorkorderQuerySet.as_manager()

    def __str__(self):
        return f"{self.site}: {self.title}"
