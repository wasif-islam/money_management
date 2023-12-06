# mod4/views.py

import requests
import yfinance as yf
from django.shortcuts import render, redirect
from datetime import datetime
from yfinance import Ticker
from .models import Stock
from django.contrib import messages
from .models import Transaction, Dividend, TransactionUpdate
from .forms import TransactionForm, DividendForm, TransactionUpdateForm
from django.conf import settings

def investment_page(request):
    # For simplicity, let's hardcode a list of stock symbols
    stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'FB', 'NFLX', 'NVDA', 'PYPL', 'GS']

    # Get stock information for each symbol
    stock_info_list = []
    for symbol in stock_symbols:
        stock = Ticker(symbol)
        stock_data = stock.history(period='1d')

        # Check if the DataFrame is empty
        if stock_data.empty or 'Close' not in stock_data.columns or 'Open' not in stock_data.columns:
            # Skip this symbol if data is not available
            continue

        latest_price = stock_data['Close'].iloc[-1]
        price_change = latest_price - stock_data['Open'].iloc[0]
        stock_info_list.append({'symbol': symbol, 'latest_price': latest_price, 'price_change': price_change})

    return render(request, 'investment_page.html', {'stock_info_list': stock_info_list})


def stock_detail(request, stock_symbol):
    try:
        # Get start and end dates from request parameters
        start_date = request.GET.get('start_date', '2021-01-01')
        end_date = request.GET.get('end_date', '2023-01-01')

        # Fetch stock data using yfinance
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

        # Check if the DataFrame is empty
        if stock_data.empty:
            raise Exception("No data available for the specified date range.")

        # Prepare data for plotting
        dates = stock_data.index.strftime('%Y-%m-%d').tolist()
        prices = stock_data['Close'].tolist()

        return render(request, 'stock_detail.html', {
            'stock_symbol': stock_symbol,
            'dates': dates,
            'prices': prices,
            'start_date': start_date,
            'end_date': end_date,
        }) 
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})


def investment_analysis(request, stock_symbol):
    stock = yf.Ticker(stock_symbol)
    
    # Get historical data
    history = stock.history(period='1d')  # Adjust the period as needed
    current_value = history['Close'].iloc[-1]  # Latest closing price
    
    # Placeholder initial investment
    initial_investment = 1000
    
    return render(request, 'investment_analysis.html', {'initial_investment': initial_investment, 'current_value': current_value, 'stock_symbol': stock_symbol})

def gain_loss_calculation(request, stock_symbol):
    stock = yf.Ticker(stock_symbol)
    
    # Get historical data
    history = stock.history(period='1d')  # Adjust the period as needed
    current_value = history['Close'].iloc[-1]  # Latest closing price
    
    # Placeholder initial investment
    initial_investment = 1000
    
    gain_loss = current_value - initial_investment
    
    return render(request, 'gain_loss_calculation.html', {'initial_investment': initial_investment, 'current_value': current_value, 'gain_loss': gain_loss, 'stock_symbol': stock_symbol})

def historical_data_trend_analysis(request, stock_symbol):
    try:
        # Fetch historical stock data using yfinance
        stock = yf.Ticker(stock_symbol)
        history = stock.history(period='1y')  # Adjust the period as needed

        # Check if the DataFrame is empty
        if history.empty:
            raise Exception("No historical data available for the specified stock.")

        # Prepare data for plotting
        dates = history.index.strftime('%Y-%m-%d').tolist()
        prices = history['Close'].tolist()

        return render(request, 'historical_data_trend_analysis.html', {
            'stock_symbol': stock_symbol,
            'dates': dates,
            'prices': prices,
        })
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import TransactionForm
from .models import Stock
import yfinance as yf

from decimal import Decimal


def record_transaction(request, stock_symbol):
    stock_info = get_stock_info(stock_symbol)
    stock = yf.Ticker(stock_symbol)
    current_value = stock.history(period='1d')['Close'].iloc[-1]
    formatted_current_value = '{:.10f}'.format(Decimal(str(current_value)))

    # Retrieve transactions related to the current stock
    transactions = Transaction.objects.filter(stock=stock_info['name'], user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.stock = stock_info['name']
            transaction.price_per_unit = formatted_current_value
            transaction.save()
            messages.success(request, 'Transaction recorded successfully.')
            return redirect('record_transaction', stock_symbol=stock_symbol)
        else:
            messages.error(request, 'Form is not valid. Please check the entered values.')
    else:
        form = TransactionForm(initial={'stock_symbol': stock_symbol, 'user_entered_stock_name': stock_info['name'], 'price_per_unit': formatted_current_value})

    return render(request, 'record_transaction.html', {'form': form, 'stock_info': stock_info, 'stock_symbol': stock_symbol, 'current_value': formatted_current_value, 'transactions': transactions})

def get_stock_info(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    stock_data = stock.info
    stock_info = {'symbol': stock_data.get('symbol', ''), 'name': stock_data.get('longName', '')}
    return stock_info


def dividend_tracking(request):
    if request.method == 'POST':
        form = DividendForm(request.POST)
        if form.is_valid():
            dividend = form.save(commit=False)
            dividend.user = request.user
            dividend.save()
            messages.success(request, 'Dividend recorded successfully.')
            return redirect('dividend_tracking')
    else:
        form = DividendForm()
    return render(request, 'dividend_tracking.html', {'form': form})

def manage_portfolios(request):
    # Add logic for managing portfolios, if needed
    return render(request, 'manage_portfolios.html')

def market_news(request):
    # Set your News API key
    news_api_key = settings.NEWS_API_KEY  # Make sure to set this in your Django settings

    # Make a request to the News API
    news_url = f'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': news_api_key,
        'category': 'business',  # You can adjust the category based on your needs
    }

    response = requests.get(news_url, params=params)
    news_data = response.json()

    # Extract relevant information from the response
    articles = news_data.get('articles', [])

    return render(request, 'market_news.html', {'articles': articles})