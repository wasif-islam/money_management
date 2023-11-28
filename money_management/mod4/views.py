# mod4/views.py

from django.shortcuts import render
import yfinance as yf
from datetime import datetime
from yfinance import Ticker



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
