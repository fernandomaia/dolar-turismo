from bs4 import BeautifulSoup
import requests

def main():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page_link = 'https://www.melhorcambio.com/cotacao/compra/dolar-turismo/sao-paulo'
    response = requests.get(page_link, timeout=5, headers=headers)
    page_content = BeautifulSoup(response.content,'html.parser')
    currency = page_content.find('span',string='R$ ')
    value = currency.find_next_sibling('span')

    return(currency.text + value.text)
