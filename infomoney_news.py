import requests
from bs4 import BeautifulSoup

def infomoney_news_api(content='mercados'):
    """
    Retrieve news articles from the InfoMoney website for a specified content category.

    Parameters:
    content (str): The content category to retrieve news articles from. Must be one of the following:
                   'mercados', 'recentes', 'global', 'investimentos', 'politica', 'economia'.
                   Default is 'mercados'.

    Returns:
    list of dict: A list of dictionaries, each containing information about a news article.
                  Each dictionary contains the following keys:
                  -'title': The title of the news article (str). e.g. 'Exportação de soja do Brasil fecha 1º semestre...'.
                  -'link': The URL to the full news article (str) e.g. 'infomoney.com.br/economia/exportacao-de-soja...'.
                  -'time': The timestamp of the news article (str) e.g. 'há 2 horas'.

    Raises:
    ValueError: If the content type provided is not in the list of valid content categories.
    """
    print('Getting news from InfoMoney...')
    content_mapping = {
        #'recentes': 'ultimas-noticias',
        'global': 'business/global',
        'mercados': 'mercados',
        'investimentos': 'onde-investir',
        'politica': 'politica',
        'economia': 'economia'
    }

    #Validating content
    if content not in content_mapping:
        raise ValueError(f"Content type '{content}' is not valid. Choose from {', '.join(content_mapping.keys())}")

    #Building URL
    mapped_content = content_mapping[content]
    url = f'https://www.infomoney.com.br/{mapped_content}/'
    
    #Requesting and parsing the page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    #Extracting news articles (title, link, time)
    news_list = []
    for item in soup.find_all('article', class_='article-card'):
        title = item.find('h3', class_='article-card__headline').text.strip()
        link = item.find('a', class_='article-card__headline-link')['href']
        time = item.find('div', class_='article-card__timestamp').find('time').text.strip()[:-1] # Removendo '.'
        news_list.append({
            'title': title,
            'link': link,
            'time': time
        })
    print('News retrieved successfully.')
    return news_list