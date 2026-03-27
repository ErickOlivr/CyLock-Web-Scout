# CyLock Web Scout

O **CyLock Web Scout** é uma ferramenta de linha de comando (CLI) desenvolvida em Python para mapeamento automatizado de URLs (*Crawling*) e auditoria passiva de cabeçalhos de segurança HTTP. 

---

## Funcionalidades

* **Web Crawler Resiliente:** Navega a partir de uma URL alvo mapeando todos os links internos, com tratamento robusto contra quedas de conexão, *timeouts* e *loops* infinitos (utilizando estruturas `Set`).
* **Scanner de Segurança Inteligente:** Analisa os *HTTP Headers* em busca de falhas de configuração, mitigando falsos positivos. Detecta:
  * Ausência ou má configuração de HSTS (*Strict-Transport-Security*).
  * Proteções legadas ou ausentes contra Clickjacking (*X-Frame-Options* e *Content-Security-Policy*).
  * Ausência total de CSP (Risco de XSS).
  * Ausência de *X-Content-Type-Options* (Risco de MIME Sniffing).
  * Ausência de *Referrer-Policy* (Vazamento de metadados e privacidade).
  * Exposição da versão do servidor (*Server*).
* **Interface de Usuário (UX) e Relatórios:** Exibe o progresso e os resultados em uma tabela interativa colorida diretamente no terminal, além de exportar relatórios padronizados em `.txt`.

---

## Como Instalar e Rodar

### Pré-requisitos
Certifique-se de ter o Python 3 instalado em sua máquina.

### Instalação
1. Clone este repositório:
```bash
git clone https://github.com/ErickOlivr/CyLock-Web-Scout.git
```
Acesse a pasta do projeto:
```bash
cd CyLock-Web-Scout
```
Instale as bibliotecas necessárias (requests, beautifulsoup4, rich):
```bash
pip install -r requirements.txt
```
### Modo de Uso
Para rodar a varredura, utilize o arquivo principal main.py passando a URL alvo com a flag -u. Você também pode usar a flag -o para gerar o relatório final.

Exemplo básico:
```bash
python main.py -u http://toscrape.com -o relatorio_toscrape.txt
```

Equipe de Desenvolvimento

### O CyLock Web Scout foi construído por uma equipe de 3 integrantes, divididos por responsabilidades e módulos:

Erick Oliveira - Code-Leader , Arquitetura, UX e Documentação de Relatórios (relatorios/exports.py)

Thierry - Engenharia do Mapeador Web (Crawler/spider.py)

Bernardo - Análise de Segurança (Auditor/scanner.py)