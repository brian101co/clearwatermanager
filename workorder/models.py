from django.db import models
from sites.models import Site
from datetime import datetime
from django.contrib.auth.models import User

class WorkOrder(models.Model):
    title = models.CharField(max_length=255)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, related_name="sites")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="managers")
    created_at = models.DateTimeField(default=datetime.now())
    description = models.TextField()
