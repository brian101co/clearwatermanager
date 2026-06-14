from django.db import models

class SiteQuerySet(models.QuerySet):
    
    def under_maintenance(self):
        return self.filter(under_maintenance=True)
    
    def operational(self):
        return self.filter(under_maintenance=False)
    
    def by_lot_numbers(self, lot_nums):
        return self.filter(identifier__in=lot_nums).order_by("identifier")



class Site(models.Model):
    LOT_TYPES = (
        ('rv', 'RV'),
        ('cabin', 'Cabin'),
        ('tent', 'Tent'),
        ('pullthrough', 'Pull Through'),
    )
        
    identifier = models.CharField(max_length=10)
    info = models.TextField()
    lot_type = models.CharField(max_length=20, choices=LOT_TYPES, default='rv')
    under_maintenance = models.BooleanField(default=False)

    # Amenities
    water = models.BooleanField(default=True)
    electric_30amp = models.BooleanField(default=True)
    electric_50amp = models.BooleanField(default=False)
    sewer = models.BooleanField(default=True)
    wifi = models.BooleanField(default=True)

    # Size
    max_length_ft = models.PositiveSmallIntegerField(null=True, blank=True)
    
    # Pricing
    nightly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    weekly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    monthly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)

    objects = SiteQuerySet.as_manager()

    def __str__(self):
        return self.identifier