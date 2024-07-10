import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta

def cdi_data():
    today = datetime.today().strftime('%d/%m/%Y')
    year_ago = (datetime.today() - timedelta(days=366*5)).strftime('%d/%m/%Y')

    url = f'https://www.bcb.gov.br/api/servico/sitebcb/bcdatasgs?tronco=estatisticas&dataInicial={year_ago}&dataFinal={today}&serie=432'
    response = requests.get(url)
    data = response.json()
    df_cdi = pd.DataFrame(data['conteudo'])
    df_cdi.columns = ['date', 'CDI']

    df_cdi['date'] = pd.to_datetime(df_cdi['date'], format='%d/%m/%Y')
    df_cdi['CDI'] = pd.to_numeric(df_cdi['CDI'], errors='coerce') / 10

    df_cdi['CDI'] = df_cdi.apply(lambda row: 0 if row['date'].day != 10 else row['CDI'], axis=1)
    df_cdi['CDI'] = (df_cdi['CDI'] / 100 + 1).cumprod()

    df_cdi.set_index('date', inplace=True)
    
    return df_cdi

def get_generic_data(): #ibov, ifix, btc, cdi
    tickers = ['BTC-USD', 'IVVB11.SA', 'SMAL11.SA', 'XFIX11.SA', '^BVSP'] # yfinance download in alphabetical order!
    df = yf.download(tickers, period='5y')['Close']

    df.columns = ['BTC-USD', 'S&P500', 'SMLL', 'IFIX', 'IBOV']
    
    df_cdi = cdi_data()
    df = pd.merge(df, df_cdi['CDI'], left_index=True, right_index=True)
    
    df = df.ffill().bfill()
    #df = df.interpolate()

    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Date'}, inplace=True)

    df.to_csv('generic_data.csv', index=False)

    return df