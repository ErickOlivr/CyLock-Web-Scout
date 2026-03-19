import datetime

def salvar_relatorio(nome_arquivo, vulnerabilidades):
    try:
        # Abre o arquivo em modo de escrita ('w') com codificação UTF-8 para aceitar acentos
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write("=" * 60 + "\n")
            arquivo.write(" RELATÓRIO DE AUDITORIA - CYLOCK WEB SCOUT\n")
            arquivo.write("=" * 60 + "\n")
            
            # Pega a data e hora exatas do sistema
            data_atual = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
            arquivo.write(f"Data do escaneamento: {data_atual}\n\n")

            # Verifica se encontrou alguma coisa
            if not vulnerabilidades:
                arquivo.write("[+] Nenhuma vulnerabilidade de cabeçalho foi detectada.\n")
            else:
                arquivo.write(f"[!] Atenção: Foram detectadas {len(vulnerabilidades)} vulnerabilidades.\n\n")
                
                # Lista cada falha de forma organizada
                for i, vuln in enumerate(vulnerabilidades, start=1):
                    arquivo.write(f"--- ALERTA #{i} ---\n")
                    arquivo.write(f"URL Afetada  : {vuln['link']}\n")
                    arquivo.write(f"Falha        : {vuln['falha']}\n")
                    arquivo.write(f"Severidade   : {vuln['severidade']}\n")
                    arquivo.write("-" * 60 + "\n")
                    
        return True

    except Exception as erro:
        # Se der problema de permissão na pasta, ele avisa
        print(f"\n[X] Erro crítico ao tentar salvar o arquivo: {erro}")
        return False