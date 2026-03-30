# CyLock Web Scout

O **CyLock Web Scout** é uma ferramenta de linha de comando (CLI) desenvolvida em Python para mapeamento automatizado de URLs (*Crawling*) e auditoria passiva de cabeçalhos de segurança HTTP. 

---

## Funcionalidades

* **Deep Web Crawler (Selenium):** Agora utiliza **Selenium WebDriver** para renderizar JavaScript. Isso permite mapear links dinâmicos que crawlers estáticos não conseguem ver.
* **Módulo Fuzzer de Diretórios:** Realiza ataques de dicionário para encontrar caminhos sensíveis como `/admin`, `/backup`, `/.env` e `/config`.
* **Filtro de Ruído Inteligente:** Implementa Expressões Regulares (Regex) para ignorar arquivos estáticos (imagens, CSS, fontes), focando a auditoria apenas em páginas HTML relevantes.
* **Scanner de Cabeçalhos (OWASP Based):** Auditoria automatizada de:
    * **HSTS:** Verifica se o transporte seguro é forçado em conexões HTTPS.
    * **Clickjacking:** Analisa `X-Frame-Options` e `Content-Security-Policy` (frame-ancestors).
    * **CSP:** Detecta ausência total ou políticas fracas (ex: `unsafe-inline`).
    * **MIME Sniffing & Referrer-Policy:** Proteção de dados e privacidade.
* **Relatórios Multiformato:** Exportação detalhada em `.txt` e `.csv` para análise posterior.

---

## Como Instalar e Rodar

### Pré-requisitos(Win)
Certifique-se de ter o Python 3 instalado em sua máquina.

### Pré-requisitos(Linux/Kali)
O sistema deve ter o **Chromium** e o **Chromium-Driver** instalados:
```bash
sudo apt update && sudo apt install chromium chromium-driver -y
```

### Instalação
1. Clone este repositório:
```bash
git clone https://github.com/ErickOlivr/CyLock-Web-Scout.git
```
2. Acesse a pasta do projeto:
```bash
cd CyLock-Web-Scout
```
3. Instale as bibliotecas necessárias (requests, beautifulsoup4, rich):
```bash
pip install -r requirements.txt
```

---

### Modo de Uso
Para rodar a varredura, utilize o arquivo principal main.py passando a URL alvo com a flag `-u`. Você também pode usar a flag `-o` para gerar o relatório final, podendo escolher entre `.txt` ou `.csv`.

Exemplo básico:
```bash
python main.py -u http://toscrape.com -o relatorio_toscrape.txt
```
```bash
python main.py -u http://toscrape.com -o relatorio_toscrape.csv
```

---

### Equipe de Desenvolvimento


Erick Oliveira - Code-Leader , Arquitetura, Fuzzer, melhorias, UX e Documentação de Relatórios

Thierry - Engenharia do Mapeador Web 

Bernardo - Análise de Segurança 
