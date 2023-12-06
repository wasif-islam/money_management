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
from django.urls import path, include  
from mod1 import views
from mod4 import views as mod4_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup, name='signup'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.loginpage,name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('reset_password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('home/',views.home,name='home'),
    path('logout/',views.logoutpage,name='logout'),
    path('link_credit_card/', views.link_credit_card, name='link_credit_card'),
    path('link_bank_account/', views.link_bank_account, name='link_bank_account'),
    path('payment_methods/', views.payment_methods, name='payment_methods'),
    path('delete_entry/', views.delete_entry, name='delete_entry'),
    path('billpay/', views.billpay, name='bill_pay'),
    path('budget/', views.budget, name='budget'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('search_bills/', views.search_bills, name='search_bills'),
    path('create_budget/', views.create_budget, name='create_budget'),
    path('investments/', mod4_views.investment_page, name='investment_page'),
    path('show_remaining_budget/<str:selected_month>/', views.show_remaining_budget, name='show_remaining_budget'),
    path('investments/', mod4_views.investment_page, name='investment_page'),
    path('stock/<str:stock_symbol>/', mod4_views.stock_detail, name='stock_detail'),
    path('investment_analysis/<str:stock_symbol>/', mod4_views.investment_analysis, name='investment_analysis'),
    path('gain_loss_calculation/<str:stock_symbol>/', mod4_views.gain_loss_calculation, name='gain_loss_calculation'),
    path('historical_data_trend_analysis/<str:stock_symbol>/', mod4_views.historical_data_trend_analysis, name='historical_data_trend_analysis'),
    path('record_transaction/', mod4_views.record_transaction, name='record_transaction'),
    #path('automatic_transaction_updates/', mod4_views.automatic_transaction_updates, name='automatic_transaction_updates'),
    path('dividend_tracking/', mod4_views.dividend_tracking, name='dividend_tracking'),
    path('manage_portfolios/', mod4_views.manage_portfolios, name='manage_portfolios'),
    path('market_news/', mod4_views.market_news, name='market_news'),
    path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # path('change_password/', views.change_password, name='change_password'),
    path('change_password/', views.MyPasswordChangeView.as_view(), name='change_password'),
    path('categorize_bill/', views.categorize_bill, name='categorize_bill'),
    path('get_expenses_for_month/<str:month>/', views.get_expenses_for_month, name='get_expenses_for_month'),
    path('payment_history/', views.payment_history, name='payment_history'),
    path('due_date_reminder/', views.due_date_reminder, name='due_date_reminder'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)