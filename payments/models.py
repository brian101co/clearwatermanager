from django.db import models
from reservations.models import Reservation
from django.utils import timezone

class PaymentQuerySet(models.QuerySet):

    def paid(self):
        return self.filter(status="paid")

    def unpaid(self):
        return self.filter(status="unpaid")
    
    def partial(self):
        return self.filter(status="partial")
    
    def by_status(self, status):
        return self.filter(status=status)
    
    def by_customer(self, customer):
        return self.filter(customer=customer)
    

class Payment(models.Model):
    STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    )
    METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('card', 'Card'),
        ('other', 'Other'),
    )

    customer = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='payments')
    amount_due = models.DecimalField(max_digits=8, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    paid_at = models.DateTimeField(null=True, blank=True)

    objects = PaymentQuerySet.as_manager()

    def __str__(self):
        return f'{self.customer.name} - {self.status}'

    def balance_due(self):
        return self.amount_due - self.amount_paid

    @property
    def is_paid(self):
        return self.status == 'paid'