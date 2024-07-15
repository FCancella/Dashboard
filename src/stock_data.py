import yfinance as yf
import pandas as pd
import utils

# def get_stock_data(ticker, df = None):
#     if not ticker.endswith('.SA'):
#         ticker = ticker + '.SA'

#     stock_data = yf.download(ticker, period='1y')['Close']

#     if df:
#         df[ticker] = stock_data # Append stock data to existing DataFrame
#     else:  
#         return stock_data

def add_stock_data(ticker, main_graph = None):
    if not ticker.endswith('.SA'):
        suffix = '.SA'
    else:
        suffix = ''

    stock_data = yf.download(ticker+suffix, period='5y')

    if main_graph is not None:
        main_graph[ticker] = stock_data['Close']
        main_graph = main_graph.ffill().bfill()
        return stock_data, main_graph
    
    return stock_data