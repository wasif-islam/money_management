from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import CustomUser
from .models import CustomBill
from .forms import CustomBillForm
from .models import CreditCard
from .forms import CreditCardForm
from .forms import BankAccountForm
from .models import Expense,Budget
from .forms import ExpenseForm,BudgetForm
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.files.storage import FileSystemStorage

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')
def loginpage(request):
    if request.method=='POST':

        if request.user.is_authenticated:
            # If the user is already authenticated, log them out
            logout(request)
        username=request.POST.get('username')
        password=request.POST.get('pass')
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Username or Password is Incorrect')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 == pass2:
            my_user = CustomUser.objects.create_user(username=uname, email=email, password=pass1, phone=phone)
            my_user.save()
            return redirect('login')
        else:
            return HttpResponse("Password do not match")

    return render(request, 'signup.html') 

def logoutpage(request):
    logout(request)
    return redirect('login')

def billpay(request):
    
    if request.method == 'POST':
        form = CustomBillForm(request.POST)
        if form.is_valid():
            custom_bill = form.save(commit=False)
            custom_bill.user = request.user  # Assign the logged-in user to the custom_bill
            custom_bill.save()
            return redirect('home')
    else:
        form = CustomBillForm()
    return render(request, 'billpay.html')

def link_credit_card(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            credit_card = form.save(commit=False)
            credit_card.user = request.user
            credit_card.save()
            return redirect('home')  
    else:
        form = CreditCardForm()

    return render(request, 'billpay.html', {'credit_card_form': form})  
def link_bank_account(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            bank_account = form.save(commit=False)
            bank_account.user = request.user
            bank_account.save()
            return redirect('home')  
    else:
        form = BankAccountForm()

    return render(request, 'billpay.html', {'bank_account_form': form})  
def budget(request):
    return render(request, 'budget.html')

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Set the user field
            expense.save()
            messages.success(request, 'Expense Added Successfully')
            return redirect('budget')
        else:
            # Print form errors for debugging
            messages.error(request, 'Invalid form data. Please check the fields.')
            return redirect('budget')

    else:
        form = ExpenseForm()

    return render(request, 'budget.html', {'form': form})

def search_bills(request):
    query = request.GET.get('q', '')
    custom_bills = CustomBill.objects.filter(bill_name__icontains=query)
    return render(request, 'billpay.html', {'custom_bills': custom_bills})


def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            
            # Get month as a string from the form
            month = form.cleaned_data['budget_month']
            
            # Combine year and month to form 'YYYY-MM' format
            budget.budget_month = month
            
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget updated successfully')
            return redirect(request.path_info)  # Redirect to the same page
    else:
        form = BudgetForm()

    return render(request, 'budget.html', {'form': form})




def show_remaining_budget(request, selected_month):
    if request.method == 'GET':
        user = request.user
        current_month_budget = Budget.objects.filter(user=user, budget_month=selected_month).first()

        if current_month_budget:
            total_expense = Expense.objects.filter(user=user, date__year=current_month_budget.created_at.year, date__month=current_month_budget.created_at.month).aggregate(Sum('amount'))['amount__sum'] or 0
            
            remaining_budget = current_month_budget.target_budget - total_expense

            if remaining_budget < 0:
                message = f'You have gone over budget by {abs(remaining_budget)}'
            else:
                message = f'Budget remaining: {remaining_budget}'

            return JsonResponse({'message': message})
        else:
            return JsonResponse({'message': f'Budget not found for {selected_month}'})
    else:
        return JsonResponse({'message': 'Invalid request'})
    

def update_profile_picture(request):
    if request.method == 'POST':
        # Exclude the password field from the form
        custom_user_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        custom_user_form.fields['password'].required = False  # Make the password field not required
        
        if custom_user_form.is_valid():
            # Save the form without validating the password
            custom_user_form.save(update_fields=['image'])
            return redirect('home')

    # Handle form errors or redirect accordingly
    return redirect('home')