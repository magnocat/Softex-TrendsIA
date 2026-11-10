# P0 — Primeiro Fluxo com LLM (Nível Avançado)

Projeto individual desenvolvido por mim na trilha de Inteligência Artificial da Softex Campinas.

## 1\. Problema e Justificativa

> **Problema:** "Eu classifico mensagens de suporte ou alertas em três níveis de prioridade (Baixa, Média, Alta) com uma justificativa de uma linha."  
> 

* **Quem possui essa necessidade:** Operadores de suporte, equipes de infraestrutura e administradores de sistemas que recebem volumosas notificações desestruturadas e precisam triar incidentes críticos com agilidade.  
* **Por que usar LLM:** Um modelo de linguagem consegue captar nuances semânticas e severidade operacional, padronizando a resposta em formato acionável.

## 2\. Tecnologias e Ambiente

* **Linguagem:** Python 3.10+ (desenvolvido e testado em Python 3.13 no Debian 13 x86\_64)  
* **Bibliotecas Principais:**  
  - `requests >= 2.31.0`: Comunicação HTTP REST com a API do LLM.  
  - `python-dotenv >= 1.0.0`: Carregamento isolado de variáveis de ambiente do arquivo `.env`.  
  - `unittest` (biblioteca padrão): Suíte automatizada de testes locais, mocks e integração real.  
  - `logging` (biblioteca padrão): Registro de auditoria operacional em arquivo local (`p0/app.log`).

## 3\. Arquitetura Modular e Parâmetros Dinâmicos

A aplicação está organizada com estrita separação de responsabilidades:

* `p0/config.py`: Carrega e valida parâmetros de conexão e **parâmetros de inferência** (temperatura, max\_tokens, repeat\_penalty) diretamente do `.env`, sem alterar o código-fonte.  
* `p0/logger.py`: Grava eventos, timestamps e latências no arquivo `p0/app.log`, com sanitização preventiva de credenciais.  
* `p0/client.py`: Monta requisições REST, controla cabeçalhos Bearer e trata falhas HTTP (401, 409, 429, 502, timeouts e conexões).  
* `p0/classifier.py`: Estruturação de prompts com raciocínio preliminar (Chain-of-Thought) para mitigar vieses de modelos leves.  
* `p0/main.py`: Interface de linha de comando (CLI) amigável que orquestra o fluxo sem expor stacktraces ao usuário.  
* `p0/tests/test_errors.py`: Suíte de testes unitários locais (offline), testes simulados com mocks e teste de chamada real.

## 4\. Como Instalar e Executar (Reprodutibilidade em Ambiente Limpo)

### Passo 1: Preparar o ambiente virtual

python3 \-m venv .venv source .venv/bin/activate

### Passo 2: Instalar dependências

pip install \-r p0/requirements.txt

### Passo 3: Configurar variáveis de ambiente

cp p0/.env.example p0/.env

# Ajuste as variáveis no arquivo p0/.env conforme seu endpoint (local ou nuvem):

# LLM\_BASE\_URL=[http\://127.0.0.1:8088/v1](http://127.0.0.1:8088/v1)

# LLM\_MODEL=qwen2.5-0.5b

# LLM\_TIMEOUT=30

# LLM\_TEMPERATURE=0.1

# LLM\_MAX\_TOKENS=100

# LLM\_REPEAT\_PENALTY=1.15

### Passo 4: Executar a aplicação

python3 p0/main.py

## 5\. Execução da Suíte de Testes

A suíte inclui testes offline (que rodam sem rede nem modelo ativo), testes de falhas simuladas via mock (401, 409, 429, timeout, queda) e teste real:

python3 \-m unittest discover \-s p0/tests \-p "test\_\*.py" \-v

## 6\. Auditoria e Logs de Execução

Todas as execuções gravam registros no arquivo `p0/app.log` contendo data, hora, latência e status HTTP, sem gravar dados sensíveis ou credenciais.

## 7\. Marcos Históricos de Entrega (Tags PBL)

- [x] **p0-basico:** Primeiro fluxo funcional conectando ao LLM local via terminal.  
- [x] **p0-intermediario:** Modularização em camadas, tratamento granular de erros HTTP e integração por Pull Request.  
- [x] **p0-avancado:** Parâmetros de inferência dinâmicos via .env, sistema de logs sanitizado, testes de lógica offline e reprodutibilidade validada.