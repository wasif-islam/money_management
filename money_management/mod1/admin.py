from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import CustomUser, CustomBill

admin.site.register(CustomUser)


@admin.register(CustomBill)
class CustomBillAdmin(admin.ModelAdmin):
    list_display = ('user', 'bill_name', 'amount', 'due_date')