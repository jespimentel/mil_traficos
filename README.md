# Mil tráficos - Piracicaba (Jan 2026)

### Escopo
Este projeto automatiza a coleta, a extração de informações e a análise com LLM de sentenças judiciais sobre tráfico de drogas em Piracicaba, extraídas do banco de sentenças (informação pública).

### Fluxo de Trabalho

**Coleta de Dados:** O script realiza web scraping com requests para baixar páginas com julgados de interesse.

**Extração de Informações:** O conteúdo HTML é processado com BeautifulSoup4 para extrair, por exemplo, número do processo, magistrado e texto completo da sentença e os organiza em dataframe, usando pandas.

**Análise com IA:** O texto de cada sentença é analisado por um modelo de linguagem (LLM), que extrai informações-chave como data do fato, local, quantidade de réus, modus operandi, alegações da defesa, resultado do processo e um resumo da decisão. Usamos o LiteLLM para facilitar a alternância dos modelos.

**Georreferenciamento:** O georreferenciamento é feito mediante consulta à api do Google.

### Faça você mesmo

- Instale as dependências necessárias (indicadas o arquivo `pyproject.toml`).

- Altere as configurações de `prepara_dados.ipynb` de acordo com o seu ambiente.

- Altere PARAMS_TJSP para analisar outros tipos de sentenças. Inspecione a página https://esaj.tjsp.jus.br/cjpg/pesquisar.do para entender como funcionam os parâmetros.

- Modifique o prompt para obter novos resultados. Faça as alterações correspondentes no JSON de saída.

- Perceba que o código contido em `prepara_dados.ipynb` cria o arquivo "csv" necessário para alimentar a aplicação. Esta, por sua vez, consiste em aplicação feita com `marimo`, que, no nosso caso, foi hospedada no GitHub.