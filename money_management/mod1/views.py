from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')
def loginpage(request):
    if request.method=='POST':
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
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1 == pass2:
            
            my_user = User.objects.create_user(uname, email,pass1)
            my_user.save()
            return redirect('login')
        else:
            return HttpResponse("Password do not match")
        
        
        
        
    return render(request, 'signup.html') 

def logoutpage(request):
    logout(request)
    return redirect('login')

def billpay(request):
    
    return render(request, 'billpay.html')