import requests

def analisar_seguranca(url_list):
    resultados = []

    for url in url_list:
        try:
            "Para adicionar mais vulnerabilidades no futuro, criaremos um novo if dentro desse bloco try"
            
            # Realizamos um GET para capturar os cabeçalhos (headers)
            response = requests.get(url, timeout=5)
            headers = response.headers
            
            #Extraindo os cabeçalhos
            xfo = headers.get("X-Frame-Options", "").upper()
            csp = headers.get("Content-Security-Policy", "").lower()
            hsts = headers.get("Strict-Transport-Security", "").lower()
            
            #1. Verificacao de ClickJacking
            seguro_xfo = "DENY" in xfo or "SAMEORIGIN" in xfo
            seguro_csp = "frame-ancestors" in csp

            if not (seguro_xfo or seguro_csp):
                resultados.append({
                    "link": url,
                    "falha": "Proteção contra Clickjacking ausente ou inválida",
                    "severidade": "Alta"
                })
                
            # 2. Verificação de HTTPS forçado (HSTS)
            if not hsts or "max-age" not in hsts:
                resultados.append({
                    "link": url,
                    "falha": "Ausência ou má configuração de HSTS",
                    "severidade": "Alta"
                })
            # 3. Verificação de Proteção contra Injeção (CSP)
            if not csp:
                resultados.append({
                    "link": url,
                    "falha": "Ausência total de CSP (Risco de XSS)",
                    "severidade": "Média"
                })
            # Armazenamos o resultado desta URL específica
        except requests.exceptions.RequestException as e:
            print(f"[-] Não foi possível auditar {url}: {e}")

    return resultados