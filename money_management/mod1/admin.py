from django.contrib import admin

# Register your models here.

from django.contrib import admin
<<<<<<< HEAD
from .models import CustomUser, CustomBill, CreditCard, BankAccount, Expense
=======
from .models import CustomUser, CustomBill, CreditCard, BankAccount
>>>>>>> c35eadc36f8459db6a107c32af42c8938f2c223d

admin.site.register(CustomUser)


@admin.register(CustomBill)
class CustomBillAdmin(admin.ModelAdmin):
    list_display = ('user', 'bill_name', 'amount', 'due_date')
    

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'cvc', 'exp_date')


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ('user', 'account_number', 'bank_name', 'branch_name')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'description', 'receipt')
=======
    list_display = ('user', 'account_number', 'bank_name', 'branch_name')
>>>>>>> c35eadc36f8459db6a107c32af42c8938f2c223d
