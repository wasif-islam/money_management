from django.contrib import admin
from .models import Stock, Transaction, AutomaticTransaction, Dividend

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['stock', 'user', 'transaction_type', 'quantity', 'price_per_unit', 'transaction_date']

@admin.register(AutomaticTransaction)
class AutomaticTransactionAdmin(admin.ModelAdmin):
    list_display = ['stock', 'user', 'transaction_type', 'amount', 'schedule']

@admin.register(Dividend)
class DividendAdmin(admin.ModelAdmin):
    list_display = ['stock', 'user', 'amount', 'dividend_date']

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name']
