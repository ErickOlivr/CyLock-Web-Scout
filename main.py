import argparse
import sys
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from Crawler.spider import extrair_links
from Auditor.scanner import analisar_seguranca
from relatorios.exports import salvar_relatorio
from relatorios.saving_in_csv import saving_in_csv
from Auditor.fuzzer import fuzzer_diretorios

console = Console()

def exibir_banner():
    banner = "[bold cyan]  Cylock Web Scout  [/bold cyan]\n[white]"
    console.print(Panel(banner, expand=False, border_style="cyan"))
    
def main():
    exibir_banner()
    
    parser = argparse.ArgumentParser(description="Mapeador e Auditor")
    parser.add_argument("-u", "--url", required=True, help="A URL alvo (ex: http://site.com)")
    parser.add_argument("-o", "--output", help="Nome do arquivo para salvar o relatório (ex: relatorio.txt)")
    
    args = parser.parse_args()
    alvo = args.url
    
    try:
        #crawler
        console.status("[bold blue]A procura de urls...[/bold blue]")
        links_encontrados = extrair_links(alvo)
        
        #Fuzzer
        with console.status("[bold blue]À procura de diretórios ocultos...[/bold blue]"):
            links_ocultos = fuzzer_diretorios(alvo)
            links_encontrados.extend(links_ocultos)
            
            links_encontrados = list(set(links_encontrados))#limpa links duplicados
            
        console.print(f"\n[bold green][+] Mapeamento finalizado![/bold green] Foram encontrados [bold yellow]{len(links_encontrados)}[/bold yellow] links no total.\n")
        
        console.print("[cyan]Links descobertos para auditoria:[/cyan]")
        for link in links_encontrados:
            console.print(f"  - {link}")
        print("\n")
            
        
        #auditor    
        with console.status("[bold magenta]Fase 2: Auditando cabeçalhos de segurança...[/bold magenta]"):
            time.sleep(2)
            
            vulnerabilidades = analisar_seguranca(links_encontrados)
        #UX
        
        #Cria tabela
        tabela = Table(title="Resultados da Auditoria")
        tabela.add_column("Link Afetado", style="cyan", no_wrap=True)
        tabela.add_column("Vulnerabilidade", style="white")
        tabela.add_column("Severidade", justify="center")
        
        for vuln in vulnerabilidades:
            cor_severidade = "red" if vuln["severidade"] == "Alta" else "yellow" if vuln["severidade"] == "Média" else "green"
            tabela.add_row(
                vuln["link"], 
                vuln["falha"], 
                f"[{cor_severidade}]{vuln['severidade']}[/{cor_severidade}]"
            )

        console.print(tabela)
        
        #Exportação(txt ou CSV)
        
        if args.output:
            console.print(f"\n[bold blue][*] Salvando relatório em {args.output}...[/bold blue]")
            if args.output.lower().endswith('.csv'):
                saving_in_csv(vulnerabilidades, args.output)
            else:
                salvar_relatorio(args.output, vulnerabilidades)
            console.print("[bold green][+] Relatório salvo com sucesso![/bold green]")

    except KeyboardInterrupt:
        console.print("\n[bold red][!] Escaneamento interrompido pelo usuário.[/bold red]")
        sys.exit(0)

if __name__ == "__main__":
    main()