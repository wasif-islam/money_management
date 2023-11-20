from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import CustomUser, CustomBill, CreditCard, BankAccount

admin.site.register(CustomUser)


@admin.register(CustomBill)
class CustomBillAdmin(admin.ModelAdmin):
    list_display = ('user', 'bill_name', 'amount', 'due_date')
    

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'cvc', 'exp_date')


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'bank_name', 'branch_name')