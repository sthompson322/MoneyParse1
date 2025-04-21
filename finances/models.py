from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
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
        return Transaction.objects.filter(category=self.category).aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')

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
