import csv

def saving_in_csv(resultados, nome_arquivo="relatorio_seguranca.csv"):
    # Verifica se há resultados para não criar um arquivo vazio à toa
    if not resultados:
        print("[!] Nenhum resultado para salvar.")
        return

    # Os cabeçalhos do CSV serão as chaves do nosso dicionário
    cabecalhos = ["link", "falha", "severidade"]

    # Abrimos o arquivo em modo de escrita ('w'). 
    # O encoding='utf-8' garante que os acentos do português fiquem corretos.
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        escritor = csv.DictWriter(arquivo_csv, fieldnames=cabecalhos)

        # Escreve a primeira linha com os nomes das colunas
        escritor.writeheader()
        
        # Escreve todos os dicionários da lista de uma vez só
        escritor.writerows(resultados)
        
    print(f"[+] Relatório salvo com sucesso em: {nome_arquivo}")