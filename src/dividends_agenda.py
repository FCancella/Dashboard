import pandas as pd
from datetime import datetime
import os
base_path = os.path.dirname(__file__)

def get_dividens_agenda():
    print('Getting dividends agenda...')
    file_path = os.path.join(base_path, 'dividends_agenda.csv')
    df = pd.read_csv(file_path)

    earliest_date = pd.to_datetime(df['Payment']).min()
    today = pd.to_datetime(datetime.today().strftime('%Y-%m-%d'))

    days_difference = (today - earliest_date).days
    if days_difference >= 7:
        df = pd.read_html('https://www.dadosdemercado.com.br/agenda-de-dividendos')[0]
        df = df[['Código', 'Tipo', 'Pagamento']]
        df.columns = ['Code', 'Type', 'Payment']

        df['Type'] = df['Type'].apply(lambda x: 'Div' if x == 'Dividendo' else ('JCP' if x == 'JCP' else 'N/A'))
        
        df['Payment'] = pd.to_datetime(df['Payment'], format='%d/%m/%Y')
        df = df[df['Payment'] >= today].reset_index(drop=True)

        # Updating the csv file with the most recent data
        df.to_csv('dividends_agenda.csv', index=False)
    
    print('Dividends agenda obtained.')