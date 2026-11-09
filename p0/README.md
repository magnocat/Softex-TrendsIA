# P0 — Primeiro Fluxo com LLM (Nível Básico)

Projeto individual desenvolvido por mim na trilha de Inteligência Artificial da Softex Campinas.

## 1\. Problema e Justificativa

> **Problema:** "Eu classifico mensagens de suporte ou alertas em três níveis de prioridade (Baixa, Média, Alta) com uma justificativa de uma linha."  
> 

* **Quem possui essa necessidade:** Operadores de suporte, equipes de infraestrutura e administradores de sistemas que recebem volumosas notificações desestruturadas e precisam triar rapidamente incidentes críticos.  
* **Por que usar LLM:** Um modelo de linguagem consegue interpretar nuances semânticas (como tom de urgência e impacto de falhas) muito melhor do que buscas estáticas por palavras-chave, gerando uma síntese padronizada.

## 2\. Configuração do Ambiente e Execução

A aplicação foi desenvolvida e testada em ambiente local (Debian 13 x86\_64).

### Pré-requisitos

* Python 3.10+  
* Endpoint de LLM compatível com a API OpenAI (utilizei o modelo local `Qwen 2.5 0.5B Instruct` via `llama-server`).

### Instalação e Execução

1. Crie e ative o ambiente virtual:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências:

```sh
pip install -r p0/requirements.txt
```

3. Configure as variáveis de ambiente:

```sh
cp p0/.env.example p0/.env
# Se necessário, ajuste LLM_BASE_URL no arquivo p0/.env
```

4. Execute o programa:

```sh
python3 p0/main.py
```

## 3\. Estado Atual da Entrega

- [x] **Nível Básico (`p0-basico`):** Entrada via terminal, requisição REST, tratamento básico e exibição estruturada.  
- [ ] **Nível Intermediário:** Modularização e testes de falha induzida.  
- [ ] **Nível Avançado:** Relatório técnico e validação de reprodutibilidade.

## 4. Solução de Problemas (Troubleshooting)

### Erro: `ModuleNotFoundError: No module named 'dotenv'` (ou `'requests'`)
* **Causa:** O script foi chamado pelo Python global do sistema operacional, fora do ambiente virtual isolado.
* **Diagnóstico:** Observe se o seu prompt no terminal possui o prefixo `(.venv)`. Se não possuir, o ambiente não está ativo.
* **Como resolver:**
  1. Ative a `.venv`:
     ```bash
     source .venv/bin/activate
     ```
  2. Garanta as dependências instaladas:
     ```bash
     pip install -r p0/requirements.txt
     ```
* **Execução direta alternativa:**
  Caso prefira executar sem ativar manualmente a `.venv`, chame o binário diretamente:
  ```bash
  ./.venv/bin/python3 p0/main.py
  