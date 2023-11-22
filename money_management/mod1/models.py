from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):  #using abstract user which by def inclds uname and pass
    
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.username
    

class CustomBill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bill_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s {self.bill_name}"
    

from .models import CustomUser

class CreditCard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, unique=True)
    cvc = models.CharField(max_length=4)
    #exp_date = models.CharField(max_length=5) 
    exp_date = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s Credit Card"

class BankAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=16, unique=True)
    bank_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s Bank Account"

class Expense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    receipt = models.ImageField(upload_to='expense_receipts/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s {self.category} Expense"
    
