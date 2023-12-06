from django import forms
from .models import CustomUser,CustomBill,CreditCard,BankAccount,Expense,Budget,BillCategory


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

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

class CustomBillForm(forms.ModelForm):
    class Meta:
        model = CustomBill
        fields = ['bill_name', 'amount', 'due_date','category']

class BillCategoryForm(forms.ModelForm):
    class Meta:
        model = BillCategory
        fields = ['category_name', 'category_description']


class CreditCardForm(forms.ModelForm):
    exp_date = forms.CharField(max_length=5, label='Expiration Date (MM/YY)', widget=forms.TextInput(attrs={'placeholder': 'Enter Expiration Date (MM/YY)'}))

    class Meta:
        model = CreditCard
        fields = ['card_number', 'cvc', 'exp_date']

    def clean_exp_date(self):
        exp_date = self.cleaned_data['exp_date']
        # Add your validation logic for MM/YY format if needed
        return exp_date

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
        labels = {
            'category': 'Expense Category',
            'amount': 'Expense Amount',
            'description': 'Expense Description',
            'receipt': 'Attach Receipt',
            'date': 'Expense Date',
        }
        help_texts = {
            'amount': 'Enter the expense amount in dollars.',
            'date': 'Select the date when the expense occurred.',
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
        labels = {
            'budget_month': 'Budget Month',
            'target_budget': 'Target Budget',
        }
        help_texts = {
            'target_budget': 'Enter the target budget for the selected month.',
        }

