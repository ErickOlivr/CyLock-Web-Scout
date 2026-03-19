from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

def extrair_links(target_url):
    links_encontrados = set()
    print(f"  [Crawler] Acessando {target_url}...")

    try:
        
        page = requests.get(target_url, timeout=30)
    
    #Se a página der erro 404 (Não Encontrado) ou 500 (Erro de Servidor), ele pula direto para o 'except'
        page.raise_for_status()
    
        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('a'):
            href = link.get('href')
            if not href or href.startswith('#'):
                continue
            
            full_link = urljoin(target_url, href)
            links_encontrados.add(full_link)
        
    except requests.exceptions.Timeout:
        print(f"  [X] O site {target_url} demorou mais de 10 segundos para responder (Timeout).")
    except requests.exceptions.ConnectionError:
        print(f"  [X] Falha de conexão. O site {target_url} pode estar fora do ar ou o link é inválido.")
    except Exception as erro:
        print(f"  [X] Erro inesperado ao acessar {target_url}: {erro}")
        
    return list(links_encontrados)
