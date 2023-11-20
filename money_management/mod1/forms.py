from django import forms
from .models import CustomUser
from .models import CustomBill


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password']


class CustomBillForm(forms.ModelForm):
    class Meta:
        model = CustomBill
        fields = ['bill_name', 'amount', 'due_date']