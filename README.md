# CyLock-Web-Scout

### 1. `main.py`
**Responsável:** Code-Leader(Erick)
* **O que faz:** É o coração do programa. A função dele é receber a URL que o usuário digitou no terminal e coordenar a ordem de execução dos outros arquivos. 
* **Como funciona:** Ele chama o `spider.py` para mapear o site, pega a lista de links devolvida, passa para o `scanner.py` auditar e, por fim, manda o `exportar.py` exibir os resultados.

### 2. `crawler/spider.py`(Thierry, Bernardo)
**Responsáveis:** Dupla de Mapeamento
* **O que faz:** É o motor de busca. A missão deste script é entrar no site alvo e extrair todos os caminhos possíveis.
* **O que você vai codar aqui:** Usando as bibliotecas `requests` e `BeautifulSoup`, você vai escrever uma função que acessa uma URL, baixa o código HTML da página e garimpa todas as tags de link (`<a href="...">`), devolvendo uma lista limpa com essas URLs descobertas.

### 3. `auditor/scanner.py`(Guilherme)
**Responsável:** Analista de Segurança
* **O que faz:** Este arquivo atua como um auditor passivo.
* **O que você vai codar aqui:** Você vai criar funções que recebem os links descobertos pelo Crawler e analisam as respostas do servidor (os *HTTP Headers*). O objetivo é usar o `requests` para verificar se faltam cabeçalhos de segurança básicos (como proteções contra Clickjacking ou ausência de forçamento HTTPS) e devolver uma lista de vulnerabilidades.

### 4. `relatorios/exportar.py`(Ian)
**Responsável:** Documentador / UX
* **O que faz:** É o responsável por pegar os dados brutos e transformá-los em algo legível para o usuário final.
* **O que você vai codar aqui:** Você vai usar a biblioteca `rich` para formatar a saída do programa no terminal (colocando alertas críticos em vermelho, informativos em azul, etc.) e criar a lógica para salvar todo o resumo do escaneamento em um arquivo `.txt` organizado.