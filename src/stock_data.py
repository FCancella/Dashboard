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
    stock_data.reset_index(inplace=True)
    stock_data = stock_data.ffill().bfill()
    stock_data = stock_data[['Date','Close']]

    if main_graph is not None:
        # stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        # stock_data.set_index('Date', inplace=True)
        # stock_data = stock_data.div(stock_data.iloc[0]).subtract(1).multiply(100).reset_index()
        # stock_data.set_index('Date', inplace=True)

        stock_data = utils.df_treatment(stock_data)


        main_graph = pd.merge(main_graph, stock_data, left_index=True, right_index=True)
        main_graph = main_graph.ffill().bfill()
        main_graph.rename(columns={'Close': ticker}, inplace=True)
        main_graph[ticker] = stock_data # Append stock data to existing DataFrame
        
        return stock_data, main_graph
    
    return stock_data