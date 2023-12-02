from django import forms
from .models import CustomUser,CustomBill,CreditCard,BankAccount,Expense,Budget


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password', 'image']

    # Add widgets to customize the form fields
    widgets = {
        'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
        'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
    }

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

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description', 'receipt', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class BudgetForm(forms.ModelForm):
    MONTH_CHOICES = [
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]

    budget_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES)
    target_budget = forms.DecimalField(label='Target Budget', required=True)

    class Meta:
        model = Budget
        fields = ['budget_month', 'target_budget']