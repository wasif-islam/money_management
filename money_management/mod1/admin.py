from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import CustomUser, CustomBill, CreditCard, BankAccount, Expense,Budget, BillCategory

admin.site.register(CustomUser)


@admin.register(CustomBill)
class CustomBillAdmin(admin.ModelAdmin):
    list_display = ('user', 'bill_name', 'amount', 'due_date','category')
    

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'cvc', 'exp_date')


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'bank_name', 'branch_name')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'description', 'receipt','date')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'budget_month', 'target_budget', 'created_at']

@admin.register(BillCategory)
class BillCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'category_name', 'category_description')