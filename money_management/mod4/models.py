from django.db import models
from mod1.models import CustomUser
# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.symbol

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use your custom user model
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=[('BUY', 'Buy'), ('SELL', 'Sell')])
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField(auto_now_add=True)

class Dividend(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use your custom user model
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    dividend_date = models.DateField(auto_now_add=True)

class TransactionUpdate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use your custom user model
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    update_type = models.CharField(max_length=15, choices=[('SPLIT', 'Stock Split'), ('MERGER', 'Merger')])
    update_date = models.DateField(auto_now_add=True)

class AutomaticTransaction(models.Model):
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use your custom user model
    transaction_type = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    schedule = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"