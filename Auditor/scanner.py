import requests
import re

def analisar_seguranca(url_list):
    resultados = []

    for url in url_list:
        try:
            "Para adicionar mais vulnerabilidades no futuro, criaremos um novo if dentro desse bloco try"
            
            # Realizamos um GET para capturar os cabeçalhos (headers)
            response = requests.get(url, timeout=5, allow_redirects=True)
            headers = response.headers
            
            url_final = response.url
            
            #Extraindo os cabeçalhos
            xfo = headers.get("X-Frame-Options", "").upper()
            csp = headers.get("Content-Security-Policy", "").lower()
            hsts = headers.get("Strict-Transport-Security", "").lower()
            xcto = headers.get("X-Content-Type-Options", "").lower()
            referrer = headers.get("Referrer-Policy", "").lower()
            server = headers.get("Server", "")
            
            #1. Verificacao de ClickJacking
            seguro_xfo = "DENY" in xfo or "SAMEORIGIN" in xfo or "ALLOW-FROM" in xfo
            seguro_csp = "frame-ancestors" in csp

            if not (seguro_xfo or seguro_csp):
                resultados.append({
                    "link": url,
                    "falha": "Proteção contra Clickjacking ausente ou inválida",
                    "severidade": "Alta"
                })
                
            # 2. Verificação de HTTPS forçado (HSTS)
            # O HSTS apenas faz sentido e é processado pelos browsers em conexões HTTPS
            if url_final.startswith("https://"):
                if not hsts or not re.search(r"max-age=\d+", hsts):
                    resultados.append({
                        "link": url,
                        "falha": "Ausência ou má configuração de HSTS",
                        "severidade": "Alta"
                    })
            else:
                # Alerta se o site não usa HTTPS, pois o HSTS não pode ser aplicado
                resultados.append({
                    "link": url,
                    "falha": "Site não utiliza HTTPS (HSTS não aplicável)",
                    "severidade": "Crítica"
                })
                
            # 3. Verificação de Proteção contra Injeção (CSP)
            if not csp:
                resultados.append({
                    "link": url,
                    "falha": "Ausência total de CSP (Risco crítico de XSS)",
                    "severidade": "Alta"  # Elevado para Alta, pois a ausência total é muito arriscada
                })
            else:
                fraquezas_csp = []
                
                tem_unsafe_inline = "'unsafe-inline'" in csp
                tem_nonce_ou_hash = re.search(r"'nonce-[^']+'|'sha(?:256|384|512)-[^']+'", csp)
                
                # Procura por diretivas perigosas conhecidas
                if tem_unsafe_inline and not tem_nonce_ou_hash:
                    fraquezas_csp.append("permite execução de scripts inline sem nonce/hash ('unsafe-inline')")
                
                if "'unsafe-eval'" in csp:
                    fraquezas_csp.append("permite execução dinâmica de código ('unsafe-eval')")
                
                if "default-src *" in csp or "script-src *" in csp:
                    fraquezas_csp.append("origem excessivamente permissiva ('*')")
                
                if fraquezas_csp:
                    motivos = " e ".join(fraquezas_csp)
                    resultados.append({
                        "link": url,
                        "falha": f"CSP fraco configurado: {motivos}",
                        "severidade": "Média"
                    })

            # 4. Verificação de MIME Sniffing
            # Separa os valores por vírgula e remove espaços para evitar falsos positivos
            valores_xcto = [x.strip() for x in xcto.split(',')]
            if "nosniff" not in valores_xcto:
                resultados.append({
                    "link": url,
                    "falha": "X-Content-Type-Options ausente (Risco de MIME Sniffing)",
                    "severidade": "Baixa"
                })

            # 5. Verificação de Referrer Policy (Privacidade)
            if not referrer:
                resultados.append({
                    "link": url,
                    "falha": "Referrer-Policy ausente (Vazamento de metadados)",
                    "severidade": "Baixa"
                })

            # 6. Exposição de Versão do Servidor
            # Só regista como falha se o cabeçalho expuser números (ex: nginx/1.18.0)
            if server and re.search(r"(\d+\.\d+|\d+h)", server):
                resultados.append({
                    "link": url,
                    "falha": f"Exposição de Servidor: {server}",
                    "severidade": "Baixa (Info)"
                })
                
            # Armazenamos o resultado desta URL específica
        except requests.exceptions.RequestException as e:
            print(f"[-] Não foi possível auditar {url}: {e}")

    return resultados