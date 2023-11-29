# mod4/views.py

from django.shortcuts import render, redirect
import yfinance as yf
from datetime import datetime
from yfinance import Ticker
from .models import Stock
from django.contrib import messages
from .models import Transaction, Dividend, TransactionUpdate
from .forms import TransactionForm, DividendForm, TransactionUpdateForm


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

def record_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction recorded successfully.')
            return redirect('record_transaction')
    else:
        form = TransactionForm()
    return render(request, 'record_transaction.html', {'form': form})


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