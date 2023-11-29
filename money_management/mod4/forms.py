# mod4/forms.py
from django import forms
from .models import Transaction, Dividend

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['stock', 'transaction_type', 'quantity', 'price_per_unit']

class DividendForm(forms.ModelForm):
    class Meta:
        model = Dividend
        fields = ['stock', 'amount']

class TransactionUpdateForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['stock', 'transaction_type', 'quantity', 'price_per_unit']
