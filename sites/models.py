from django.db import models

class Site(models.Model):
    identifier = models.CharField(max_length=10)
    info = models.TextField()

    def __str__(self):
        return self.identifier