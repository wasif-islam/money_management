from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm #eta MH add korse
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
        form = UserProfileForm(request.POST)
        if form.is_valid():
            #user_instance = form.save(commit=False)
            pass1 = form.cleaned_data['password1']
            pass2 = form.cleaned_data['password2']
            

            if pass1 == pass2:
                user_instance = form.save(commit=False)
                user_instance.set_password(pass1)  # Set the user's password
                user_instance.save()
                login(request, user_instance) #log user in aftr signup
                return redirect('login')
            else:
                return HttpResponse("Password does not match")
    else:
        form = UserProfileForm()

    return render(request, 'signup.html', {'form': form})
        
        
        
        
    #return render(request, 'signup.html') 

def logoutpage(request):
    logout(request)
    return redirect('login')