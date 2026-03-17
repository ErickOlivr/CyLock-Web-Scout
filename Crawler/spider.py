from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

def extrair_links(target_url):
    url_list = []

    page = requests.get(target_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_link = urljoin(target_url, href)
            url_list.append(full_link)

    return list(set(url_list))

print(extrair_links('https://www.scrapethissite.com/pages/forms/'))