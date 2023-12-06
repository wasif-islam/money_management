# mod4/forms.py
from django import forms
from .models import Transaction, Dividend, Stock


class TransactionForm(forms.ModelForm):
    TRANSACTION_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]

    transaction_type = forms.ChoiceField(choices=TRANSACTION_CHOICES)
    stock_name = forms.CharField(max_length=255, label='Stock Name', required=False)
    price_per_unit = forms.DecimalField(max_digits=20, decimal_places=10)

    class Meta:
        model = Transaction
        fields = ['stock_name', 'transaction_type', 'quantity', 'price_per_unit']

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)

        if 'stock_name' in self.initial:
            self.fields['stock_name'].initial = self.initial['stock_name']

        if 'price_per_unit' in self.initial:
            self.fields['price_per_unit'].initial = self.initial['price_per_unit']

    def clean(self):
        cleaned_data = super().clean()
        stock_name = cleaned_data.get('stock_name')

        if stock_name:
            cleaned_data['stock'] = stock_name

        return cleaned_data



class DividendForm(forms.ModelForm):
    class Meta:
        model = Dividend
        fields = ['stock', 'amount']

class TransactionUpdateForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['stock', 'transaction_type', 'quantity', 'price_per_unit']
