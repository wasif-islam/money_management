"""
URL configuration for money_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mod1 import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup, name='signup'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.loginpage,name='login'),
    path('home/',views.home,name='home'),
    path('logout/',views.logoutpage,name='logout'),
    path('link_credit_card/', views.link_credit_card, name='link_credit_card'),
    path('link_bank_account/', views.link_bank_account, name='link_bank_account'),
    path('billpay/', views.billpay, name='bill_pay'),
    path('budget/', views.budget, name='budget'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('search_bills/', views.search_bills, name='search_bills'),
    path('create_budget/', views.create_budget, name='create_budget'),
    path('show_remaining_budget/<str:selected_month>/', views.show_remaining_budget, name='show_remaining_budget'),
    


]
