from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .models import CustomBill
from .forms import CustomBillForm
from .models import CreditCard
from .forms import CreditCardForm
from .forms import BankAccountForm
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