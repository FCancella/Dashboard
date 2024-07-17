import numpy as np
import pandas as pd
import yfinance as yf

def ewma_volatility(serie, lbda = 0.94):
    #return data.ewm(span=lbda).std()

    # gera uma lista decrescente do número total de elementos menos um até 0
    i = np.arange(len(serie)-1, -1, -1)
    
    # aplicação da formula para gerar a variância
    var = ((1 - lbda) * lbda ** i * serie ** 2).sum()
    
    # calcula a raiz da variância 
    vol = np.sqrt(var)
    return vol

def portfolio_volatility(df, volumes, ewma = True):
    df = df.pct_change().dropna()
    # series de retorno em np array
    series = df.T.values
    # gera os pesos
    weights = np.array(volumes) / sum(volumes)
    # gera a matriz de correlação
    correlation_matrix = np.corrcoef(series)

    # calcula a volatilidade de cada ativo da carteira (por ewma ou std)
    volatilities = np.array([ewma_volatility(x) if ewma else x.std() for x in series])
    
    # faz a multiplicação das matrizes para calcular a variancia do portfolio
    var = np.matmul(np.matmul(volatilities * weights, correlation_matrix), volatilities * weights)
    
    portfolio_volatility = np.sqrt(var)
    return portfolio_volatility

def get_portfolio_vol(df, ewma = True):
    print('Getting portfolio volatility...')
    df = pd.DataFrame(df)
    volumes = np.array(df['Weight'])
    tickers = df['Stock'].str.extract(r'\(([^)]+)\)')[0].tolist() # caracteres entre parenteses
    tickers = [x + '.SA' for x in tickers]
    
    portfolio_df = yf.download(tickers, period='2y')['Adj Close']
    print('Portfolio data downloaded.')
    return portfolio_volatility(portfolio_df, volumes, ewma)