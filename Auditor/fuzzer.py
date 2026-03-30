import requests
from urllib.parse import urljoin

"""
FUNCIONALIDADE: Descoberta Ativa de Diretórios.
Realiza requisições HTTP diretas para caminhos sensíveis predefinidos.
Identifica ativos que não possuem links públicos, como painéis ADM e backups.
"""

def fuzzer_diretorios(target_url):
    wordlist = ["admin", "login", "config", ".env", "backup", "api/v1", "db"]
    encontrados = []
    
    # Itera sobre a wordlist: baseada nos caminhos mais visados em ataques reais
    for path in wordlist:
        base_url = target_url if target_url.endswith('/') else target_url + '/'
        url_teste = urljoin(base_url, path)
        try:
            # O uso de allow_redirects=False impede que o servidor mascare um 404 como um 200 (Home)
            response = requests.get(url_teste, timeout=3, allow_redirects=False)
            if response.status_code == 200:
                print(f"  [+] Diretório encontrado: {url_teste}")
                encontrados.append(url_teste)
        except Exception:
            continue
    return encontrados