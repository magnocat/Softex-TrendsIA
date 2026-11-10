P0 — Relatório de Execução
Autor: Magno Fernando da Fonseca Projeto: P0 — Primeiro Fluxo com LLM (Classificador de Mensagens e Alertas de Suporte)


1. Evolução por Nível
Nível Básico (p0-basico): Eu construí o núcleo funcional mínimo da aplicação em Python. Estruturei a captura de entrada de texto pelo terminal, realizei a chamada REST direta ao endpoint local do LLM (llama-server rodando o modelo Qwen 2.5 0.5B Instruct no Node03), tratei a resposta e exibi a classificação na tela. Garanti o isolamento de variáveis com .env e publiquei o repositório no GitHub.

Nível Intermediário (p0-intermediario): Eu refatorei a aplicação separando estritamente as responsabilidades em quatro módulos (config.py, client.py, classifier.py e main.py). Implementei bloqueio de entradas vazias e tratamento amigável de erros previsíveis (HTTP 401 de autenticação, HTTP 429 de cota, HTTP 409 de conflito, timeout de 30s e quedas de conexão). Criei uma suíte com 8 testes automatizados (combinando mocks para falhas simuladas e teste real) e integrei essa evolução via branch e Pull Request.

Nível Avançado (p0-avancado): Eu tornei a aplicação configurável dinamicamente via .env (permitindo ajustar temperature, max_tokens e repeat_penalty sem alterar código). Implementei um sistema de auditoria e logging (logger.py) que grava métricas e latência em p0/app.log sem expor dados sensíveis. Adicionei testes de lógica local offline e validei a instalação e execução em ambiente limpo do zero.


2. Decisões Principais
Decisão 1: Utilização de Requisições REST Nativas (requests) em vez do SDK da OpenAI
Decisão Tomada: Utilizar a biblioteca requests para realizar chamadas HTTP diretas ao endpoint /v1/chat/completions.
Alternativa Considerada: Instalar o pacote oficial openai em Python.
Justificativa: A chamada REST direta torna a comunicação transparente, facilita o controle de timeouts, cabeçalhos e inspeção granular de códigos de status HTTP (401, 409, 429), demonstrando de forma mais nítida a competência C03 sem camadas de abstração desnecessárias.
Decisão 2: Execução de LLM Local (llama-server) na Infraestrutura Física Própria (Node03)
Decisão Tomada: Hospedar o modelo Qwen 2.5 0.5B Instruct localmente no servidor Debian 13.
Alternativa Considerada: Usar exclusivamente APIs pagas em nuvem ou depender da fila do LLM institucional.
Justificativa: Garantir custo zero de tokens, autonomia completa para testes adversos ilimitados e compreensão prática do comportamento de inferência em hardware real com CPU.
Decisão 3: Estruturação com Raciocínio Preliminar (Chain-of-Thought Invertido)
Decisão Tomada: Forçar o modelo a responder primeiro se há risco e o tipo do chamado antes de emitir a palavra da prioridade.
Alternativa Considerada: Prompt direto pedindo apenas a prioridade no primeiro token.
Justificativa: Modelos ultraleves (500M) sofrem de viés de tendência central e cravavam "Média" para qualquer texto. A indução do raciocínio prévio aumentou a sensibilidade para casos críticos.


3. Testes e Resultados
Teste
Entrada ou Situação
Resultado Esperado
Resultado Obtido
T01: Entrada Válida (Crítica)
"um galho caiu e derrubou a rede"
Classificar como Alta com justificativa
Prioridade: Alta (Emergência com impacto)
T02: Entrada Válida (Leve)
"trocar galão de água é com vcs?"
Classificar como Baixa
Prioridade: Baixa (Dúvida sem risco)
T03: Entrada Válida (Hardware)
"a impressora travou papel"
Classificar como Média
Prioridade: Média (Falha operacional simples)
T04: Entrada Vazia
Espaços em branco ("   ")
Bloqueio imediato com aviso amigável
Bloqueado: "Entrada Rejeitada: O texto informado está vazio."
T05: Credencial Inválida (Mock)
Simulação de resposta HTTP 401
Interrupção controlada orientando checar API_KEY
Exceção capturada: "Credencial ausente ou inválida (HTTP 401)"
T06: Cota Excedida (Mock)
Simulação de resposta HTTP 429
Aviso amigável de limite de requisições
Exceção capturada: "Limite de cota ou taxa excedido (HTTP 429)"
T07: Conflito de Estado (Mock)
Simulação de resposta HTTP 409
Aviso de conflito de parâmetros
Exceção capturada: "Conflito na requisição (HTTP 409)"
T08: Queda do Serviço (Mock)
Simulação de ConnectionError
Mensagem indicando servidor inativo
Exceção capturada: "Falha de conexão com endpoint"
T09: Timeout de Rede (Mock)
Demora acima do tempo limite configurado
Interrupção segura avisando timeout
Exceção capturada: "Tempo limite excedido"
T10: Lógica Local (Offline)
Validação da montagem do payload REST
Payload montado sem tocar na rede
Sucesso: parâmetros validados desconectado



4. Falhas e Limitações
Falha 1: Timeout de 15 segundos nos Testes Iniciais
O que aconteceu: O teste de execução real falhava por estouro de timeout (ReadTimeoutError).
Como foi identificado: O log de erro do unittest registrou que a chamada levou 15.1 segundos.
Como foi tratado: Identifiquei que o hardware do Node03 (Intel Core i5-2410M rodando em CPU) levava tempo excessivo para processar prompts com mais de 300 tokens. Simplifiquei o prompt de sistema para cerca de 60 tokens e aumentei o timeout configurável para 30 segundos no .env.
Situação: Totalmente corrigido.
Falha 2: Viés de Primazia e Alucinações Semânticas no Qwen 0.5B
O que aconteceu: O modelo classificou "o céu tá claro hoje" como Prioridade Alta e justificou que "meu chefe morreu é problema técnico sem risco".
Como foi identificado: Durante os testes manuais exploratórios no terminal.
Como foi tratado: Implementei Chain-of-Thought no prompt para forçar análise de risco antes da classificação.
Por que permanece: Embora o raciocínio prévio tenha corrigido casos graves, modelos ultraleves (500M) têm limitações cognitivas intrínsecas e continuam vulneráveis ao viés da primeira opção listada. A solução definitiva requer modelos a partir de 3B ou 8B parâmetros, o que foi documentado como limitação conhecida da infraestrutura.


5. Uso de IA no Desenvolvimento
Ferramenta Utilizada: Gemini (Task Mode via Chat / Assistente).
Tarefas Delegadas: Estruturação da arquitetura modular do código, elaboração da suíte de testes simulados com mocks (unittest.mock), sugestão de técnicas de engenharia de prompt (Chain-of-Thought) e apoio na formatação da documentação.
Resultado Aproveitado: A divisão de responsabilidades em config, client, classifier e logger, além dos testes parametrizados.
Correções e Alterações Realizadas por Mim: Identifiquei e exigi a remoção de valores hardcoded no config.py, orientei a inclusão de testes específicos para HTTP 409 e 429, rejeitei formatações que quebravam o terminal e diagnostiquei manualmente as causas do timeout no hardware do Node03.
Forma de Verificação: Execução manual de cada comando no terminal do Node03, validação cruzada dos commits no GitHub e execução da suíte automatizada de testes com verificação de logs.


6. Reflexão Final
Principal Aprendizado: Compreendi na prática que o sucesso de uma solução com LLM não depende apenas do código de integração, mas profundamente da capacidade do modelo e de como o prompt é estruturado. Vi na prática como a geração autorregressiva pode induzir o modelo a alucinar para justificar um token gerado precipitadamente.
Competência mais Desenvolvida: C03 (Integração e resiliência com APIs REST) e C01 (Estruturação e organização de código Python), ao tratar todas as variações de falhas de transporte e isolar a aplicação em camadas profissionais.
Aspecto que Precisa ser Aprimorado: Técnicas de avaliação sistemática com datasets padronizados (benckmarking automatizado), superando a avaliação puramente manual para os próximos projetos (P1 e P2).