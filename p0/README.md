# P0 — Primeiro Fluxo com LLM (Nível Intermediário)

Projeto individual desenvolvido por mim na trilha de Inteligência Artificial da Softex Campinas.

## 1\. Problema e Justificativa

> **Problema:** "Eu classifico mensagens de suporte ou alertas em três níveis de prioridade (Baixa, Média, Alta) com uma justificativa de uma linha."  
> 

* **Quem possui essa necessidade:** Operadores de suporte, equipes de infraestrutura e administradores de sistemas que recebem volumosas notificações desestruturadas e precisam triar incidentes críticos com agilidade.  
* **Por que usar LLM:** Um modelo de linguagem consegue captar nuances semânticas e severidade operacional, padronizando a resposta em formato acionável.

## 2\. Arquitetura e Modularização (Nível Intermediário)

O código foi refatorado para garantir a separação estrita de responsabilidades:

* p0/config.py: Carregamento e validação de configurações e variáveis de ambiente.  
* p0/client.py: Preparação de payloads, controle de autenticação (Bearer token) e transporte HTTP REST.  
* p0/classifier.py: Estruturação de prompts, regras de negócio e validação semântica das respostas.  
* p0/main.py: Captura de entrada pelo terminal, orquestração e apresentação visual amigável.  
* p0/tests/test\_errors.py: Suíte de testes automatizados unitários e de integração.

## 3\. Tratamento de Erros e Resiliência

A aplicação trata de forma amigável e segura (sem expor segredos ou stacktraces):

* Entradas vazias: Rejeição imediata antes de acionar a rede.  
* Autenticação (HTTP 401/403): Alerta orientando conferir LLM\_API\_KEY.  
* Indisponibilidade / Falha de Conexão: Mensagem clara indicando se o serviço está desligado.  
* Timeout: Tratamento do limite de tempo de espera.  
* Resposta Malformada: Validação estrutural do JSON retornado.

## 4\. Testes Reais vs. Testes Simulados (Mocks)

* Testes Reais: Executados ponta a ponta contra o modelo local Qwen 2.5 0.5B Instruct no Node03.  
* Testes Simulados (Mocks): Para demonstrar cenários de falha técnica (como credencial inválida 401, timeout e queda de servidor) sem depender de quebrar a infraestrutura real, utilizamos unittest.mock.

Comando para executar a suíte de testes: python3 \-m unittest discover \-s p0/tests \-p "test\_\*.py" \-v

## 5\. Exemplos de Entrada e Saída Observados

* Exemplo 1:  
  - Entrada: "Minha impressora travou"  
  - Saída: Prioridade: Média \| Justificativa: Falha de impressão sem impacto sistêmico imediato.  
* Exemplo 2:  
  - Entrada: "Servidor de banco de dados principal parou de responder e a aplicação caiu"  
  - Saída: Prioridade: Alta \| Justificativa: Queda de componente crítico com indisponibilidade total do serviço.

## 6\. Solução de Problemas (Troubleshooting)

* Erro ModuleNotFoundError: No module named 'dotenv' ou 'requests'  
  - Causa: Script executado fora do ambiente virtual isolado.  
  - Como resolver: Ative o ambiente virtual antes de executar (source .venv/bin/activate).  
  - Execução direta alternativa: ./.venv/bin/python3 p0/main.py

## 7\. Estado Atual da Entrega

- [x] Nível Básico (p0-basico): Núcleo funcional da chamada ao LLM.  
- [x] Nível Intermediário (p0-intermediario): Modularização, tratamento granular de erros, suíte de testes e integração via Pull Request.  
- [ ] Nível Avançado (p0-avancado): Validação em ambiente limpo, reprodutibilidade e relatório final.