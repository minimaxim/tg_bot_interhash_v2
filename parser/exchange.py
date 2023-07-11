from bs4 import BeautifulSoup

import requests

def curs():
    url = 'https://ru.investing.com/currencies/usd-rub'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    exchange_rate_block = soup.find('span', class_='text-2xl')
    exchange_rate = exchange_rate_block.text.strip()
    exchange_rate = float(exchange_rate.replace(',', '.'))

    return int(exchange_rate + 1)
