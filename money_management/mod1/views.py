from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import CustomUser
from .models import CustomBill,BillCategory
from .forms import CustomBillForm, BillCategoryForm
from .models import CreditCard
from .forms import CreditCardForm
from .forms import BankAccountForm
from .models import Expense,Budget
from .forms import ExpenseForm,BudgetForm
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from django.http import HttpResponseBadRequest, JsonResponse,HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import UserRegistrationForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.db.models import Sum
import calendar
from calendar import monthrange


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
    print("Inside signup view")
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False  # User is not active until email confirmation

            user.save()

            # Send email for confirmation
            send_activation_email(request, user)

            messages.success(request, 'Please check your email to complete authentication. Please make sure you check the spam folder as well.')

            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'signup.html', {'form': form})

def send_activation_email(request, user):
    current_site = get_current_site(request)
    
    # Convert the bytes to a string using decode()
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Create the activation link
    activation_link = f'http://{current_site.domain}/activate/{uidb64}/{default_token_generator.make_token(user)}/'

    subject = 'Activate Your Account'
    message = f'Hi {user.username},\n\nClick the following link to activate your account:\n\n{activation_link}\n\nIf you did not register on our site, please ignore this email.\n\nThanks!'
    
    from_email = 'needspeed3600@gmail.com'  # Replace with your email
    to_email = 'needspeed3600@gmail.com'  # Replace with the specific email
    
    send_mail(subject, message, from_email, [to_email])

def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        # Log in the user after activation
        authenticated_user = authenticate(request, username=user.username, password=user.password)
        login(request, authenticated_user)

        messages.success(request, 'Your account has been activated. You are now logged in.')

        return redirect('home')
    else:
        messages.error(request, 'Invalid activation link.')
        return HttpResponse('Activation link is invalid!')
# views.py

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils import timezone
from django.conf import settings

class ActivateAccountView(PasswordResetConfirmView):
    template_name = 'activation_template.html'
    success_url = '/login/'
    
    def form_valid(self, form):
        user = form.save()
        user.is_active = True
        user.save()
        authenticated_user = authenticate(self.request, username=user.username, password=user.password)
        login(self.request, authenticated_user)

        messages.success(self.request, 'Authentication Successful, Welcome to Money Management.')

        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expiration_time'] = settings.PASSWORD_RESET_TIMEOUT // 60  # Convert seconds to minutes
        return context

    def get_user(self, uidb64):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    def get_uidb64(self):
        return self.kwargs.get(self.uidb64_url_kwarg)

# @login_required(login_url='login')  #changing pass
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important to keep the user logged in
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('home')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'change_password.html', {'form': form})
class MyPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('home')  # Redirect to home upon successful password change

def logoutpage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def billpay(request):
    # Check if default categories exist, create them if not
    default_categories = ['Utilities', 'Entertainment', 'Food']
    for category_name in default_categories:
        category, created = BillCategory.objects.get_or_create(
            user=request.user,
            category_name=category_name,
            defaults={'category_description': f'Default category for {category_name.lower()} expenses.'}
        )

    categories = BillCategory.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CustomBillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user

            selected_category_id = request.POST.get('bill_category')
            selected_category = BillCategory.objects.get(pk=selected_category_id)
            bill.category = selected_category

            bill.save()
            return redirect('bill_pay')
    else:
        form = CustomBillForm()

    return render(request, 'billpay.html', {'form': form, 'categories': categories})

def categorize_bill(request):
    print("categorize_bill method called")
    if request.method == 'POST':
        form = BillCategoryForm(request.POST)
        if form.is_valid():
            # Save the new category
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            print("Category saved successfully")
            return redirect('bill_pay')  # Redirect to the billpay page
    else:
        form = BillCategoryForm()

    return render(request, 'billpay.html', {'form': form})

@login_required
def link_credit_card(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            credit_card = form.save(commit=False)
            credit_card.user = request.user
            credit_card.save()
            return redirect(request.path_info)  
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
            
            # Redirect to a specific URL after saving the budget
            return redirect(request.path_info)
  # Replace 'your_redirect_url_name' with the actual URL name
    else:
        form = BudgetForm()

    return render(request, 'budget.html', {'form': form})




def show_remaining_budget(request, selected_month):
    if request.method == 'GET':
        user = request.user

        # Find the budget for the selected month
        current_month_budget = Budget.objects.filter(user=user, budget_month=selected_month).first()

        if current_month_budget:
            # Calculate the first and last day of the selected month
            first_day = f'{current_month_budget.created_at.year}-{selected_month}-01'
            last_day = f'{current_month_budget.created_at.year}-{selected_month}-{monthrange(current_month_budget.created_at.year, int(selected_month))[1]}'

            # Calculate total expense for the selected month
            total_expense = Expense.objects.filter(
                user=user,
                date__range=[first_day, last_day]
            ).aggregate(Sum('amount'))['amount__sum'] or 0

            # Calculate remaining budget
            remaining_budget = current_month_budget.target_budget - total_expense
            percentage_remaining = (remaining_budget / current_month_budget.target_budget) * 100 if current_month_budget.target_budget != 0 else 0

            return JsonResponse({
                'remaining_budget': remaining_budget,
                'percentage_remaining': percentage_remaining,
                'budget_month': current_month_budget.budget_month,
                'target_budget': current_month_budget.target_budget,
            })
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