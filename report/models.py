from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    source = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id) + " - Transaction from -" + self.source

class Income(Transaction):
    def __str__(self):
        return str(self.id) + " - Income from -" + self.source

class Expense(Transaction):
    def __str__(self):
        return str(self.id) + " - Expense for -" + self.source