import requests

def analisar_seguranca(url_list):
    resultados = []

    for url in url_list:
        try:
            "Para adicionar mais vulnerabilidades no futuro, criaremos um novo if dentro desse bloco try"
            
            # Realizamos um GET para capturar os cabeçalhos (headers)
            response = requests.get(url, timeout=5)
            headers = response.headers
            
            vulnerabilidades = []

            # 1. Verificação de Clickjacking 
            if "X-Frame-Options" not in headers:
                vulnerabilidades.append("Ausência de X-Frame-Options (Risco de Clickjacking)")

            # 2. Verificação de HTTPS forçado (HSTS)
            if "Strict-Transport-Security" not in headers:
                vulnerabilidades.append("Ausência de HSTS (Site pode permitir conexões inseguras)")

            # 3. Verificação de Proteção contra Injeção (CSP)
            if "Content-Security-Policy" not in headers:
                vulnerabilidades.append("Ausência de CSP (Risco de XSS)")

            # Armazenamos o resultado desta URL específica
            resultados.append({
                "url": url,
                "status": response.status_code,
                "falhas": vulnerabilidades
            })

        except requests.exceptions.RequestException as e:
            print(f"[-] Não foi possível auditar {url}: {e}")

    return resultados

"A partir dessa linha é só um teste, será apagado depois de desenvolver todo o scanner"
if __name__ == "__main__":
    links_teste = ["https://www.google.com", "http://www.ufs.br"]
    relatorio = analisar_seguranca(links_teste)
    
    for item in relatorio:
        print(f"\nAlvo: {item['url']}")
        if item['falhas']:
            for falha in item['falhas']:
                print(f"  [!] {falha}")
        else:
            print("  [+] Nenhum problema básico encontrado.")