from django.db import models
from sites.models import Site
from django.utils import timezone
from django.contrib.auth.models import User

class WorkOrder(models.Model):
    title = models.CharField(max_length=255)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, related_name="sites")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="managers")
    created_at = models.DateTimeField(default=timezone.now())
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.site}: {self.title}"