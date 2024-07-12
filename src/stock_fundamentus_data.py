import requests
from bs4 import BeautifulSoup

def get_fundamentus_data(ticker):
    """
    Retrieves fundamental data for a specific stock from the Fundamentus website.

    Parameters:
    ticker (str): The stock ticker symbol for which data will be retrieved.

    Returns:
    dict: A dictionary containing the following fundamental data:
        - P/L: Price to Earnings ratio.
        - P/VP: Price to Book Value ratio.
        - DY: Dividend Yield.
        - ROE: Return on Equity.
        - ROIC: Return on Invested Capital.
    """
    print("Getting fundamentus for", ticker)
    url = f"https://www.fundamentus.com.br/detalhes.php?papel={ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    data = {}

    data['P/L'] = soup.find(string="P/L").find_next('span').text.strip()
    data['P/VP'] = soup.find(string="P/VP").find_next('span').text.strip()
    data['DY'] = soup.find(string="Div. Yield").find_next('span').text.strip()
    data['ROE'] = soup.find(string="ROE").find_next('span').text.strip()
    data['ROIC'] = soup.find(string="ROIC").find_next('span').text.strip()

    print("Fundamentus data retrieved successfully.")

    return data
