from django import forms
from .models import CustomUser
from .models import CustomBill
from .models import CreditCard
from .models import BankAccount

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password']


class CustomBillForm(forms.ModelForm):
    class Meta:
        model = CustomBill
        fields = ['bill_name', 'amount', 'due_date']


class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['card_number', 'cvc', 'exp_date']

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_number', 'bank_name', 'branch_name']