from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import re
import time
import os

"""
FUNCIONALIDADE: Mapeador Web Avançado (Crawler).
Utiliza Selenium para renderizar JavaScript, permitindo encontrar links em Single Page Applications (SPAs).
Implementa filtros de Regex para evitar o escaneamento de arquivos estáticos (lixo/ruído).
"""

def extrair_links(target_url):
    links= set()
    # Configurações de "Hardening" para rodar o navegador em ambientes Linux/VM
    options = Options()
    options.add_argument("--headless") # Roda sem abrir a janela do navegador

    # DETECÇÃO AUTOMÁTICA DE SISTEMA OPERACIONAL
    if os.name == 'nt':  # 'nt' significa que o sistema é Windows
        # No Windows, o webdriver-manager baixa e configura o driver sozinho
        servico = Service(ChromeDriverManager().install())
    else:
        # No Linux (Kali), usamos o caminho nativo que instalamos via apt
        options.binary_location = "/usr/bin/chromium"
        servico = Service("/usr/bin/chromedriver")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=servico, options=options)
    

    try:
        driver.get(target_url)
        time.sleep(3) # Dá tempo para o JS carregar
        
        html_renderizado = driver.page_source
        soup = BeautifulSoup(html_renderizado, 'html.parser')
        
        # Procura em MÚLTIPLAS tags
        for tag in soup.find_all(['a', 'form', 'iframe', 'script']):
            link = tag.get('href') or tag.get('action') or tag.get('src')
            if link and not link.startswith(('#', 'javascript:', 'mailto:')):
                links.add(urljoin(target_url, link))
                
        # Técnica de "Deep Scraping": Busca links em tags HTML e também via Regex no código bruto
        # Isso permite capturar endpoints de API escondidos em variáveis JavaScript
        padrao_caminhos = re.findall(r'["\'](/[\w\.\-/]+)["\']', html_renderizado)
        for caminho in padrao_caminhos:
            links.add(urljoin(target_url, caminho))
            
    except Exception as e:
        print(f"  [X] Erro ao extrair links com Selenium: {e}")
    finally:
        driver.quit()
        
    padrao_ignorados = re.compile(r'\.(jpg|jpeg|png|webp|gif|svg|ico|css|js|woff|woff2|ttf|eot|mp4|mp3|pdf)(?:$|\?|/)')
    
    links_limpos = []
    
    for link in links:
        # Filtro de Eficiência: Remove imagens, CSS e fontes para focar apenas em páginas auditáveis
        if not padrao_ignorados.search(link.lower()):
            links_limpos.append(link)
            
    return links_limpos