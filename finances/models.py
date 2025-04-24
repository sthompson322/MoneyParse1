from django.db import models
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse
from .constants import CATEGORY_CHOICES

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Income - ${self.amount}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    with_who_or_what = models.CharField(max_length=100, blank=True)
    date = models.DateField()

    def __str__(self):
        sign = "+" if self.type else "-"
        return f"{sign} {self.category} - ${self.amount}"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    limit = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def spent(self):
        return Transaction.objects.filter(user=self.user, category=self.category, type=False).aggregate(
            total=Sum('amount')
        )['total'] or Decimal(0.00)

    @property
    def remaining(self):
        return self.limit - self.spent

    @property
    def percent_used(self):
        if self.limit > 0:
            return (self.spent / self.limit) * 100
        return 0


    def __str__(self):
        return f"{self.category} - ${self.limit} - ${self.spent}"

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.subject} ({self.status})"

    def get_absolute_url(self):
        return reverse('finances.profile')

    def get_delete_url(self):
        return reverse('finances.delete_ticket', args=[self.id])

    def get_edit_url(self):
        return reverse('finances.edit_ticket', args=[self.id])