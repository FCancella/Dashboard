import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from io import StringIO
import os
base_path = os.path.dirname(__file__)

DATA_FILE = os.path.join(base_path, 'recommended_portfolios.json')
DATE_FORMAT = '%Y-%m-%d'

def most_recent_recommended_portfolio_url():
    url = 'https://br.advfn.com/jornal/carteira-recomendada/carteira-mensal'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    for link in soup.find_all('a', class_='post-title')[:10]:
        if 'ações' in link.text.lower().split():
            return link['href']

    return None

def scrape_recommended_portfolios():
    print('Scraping recommended portfolios...')
    url = most_recent_recommended_portfolio_url()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    portfolios = {}
    for h2 in soup.find('div', class_='post-content post-dymamic').find_all('h2')[2:]:
        table = h2.find_next('table')
        owner = h2.text.strip()
        if table:
            df = pd.read_html(StringIO(str(table)))[0]
            df = df.loc[1:].reset_index(drop=True)
            if len(df.columns) == 1:
                df.columns = ['Stock']
                df['Weight'] = 100.0 / len(df)
            else:
                df.columns = ['Stock', 'Weight']
                df['Weight'] = df['Weight'].str.replace('%', '').astype(float)
            portfolios[owner] = df.to_dict(orient='records')

    data = {
        'timestamp': datetime.now().strftime(DATE_FORMAT),
        'portfolios': portfolios
    }
    
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

    print('Recommended portfolios scraped and saved.')
    return portfolios

def load_recommended_portfolios():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            timestamp = datetime.strptime(data['timestamp'], DATE_FORMAT)
            if datetime.now().month != timestamp.month or datetime.now().year != timestamp.year:
                return scrape_recommended_portfolios()
            return data['portfolios']
    else:
        return scrape_recommended_portfolios()

# portfolios = load_recommended_portfolios()
# for owner, portfolio in portfolios.items():
#     print(f'Portfolio of {owner}:')
#     df = pd.DataFrame(portfolio)
#     print(df)
#     print('\n')
