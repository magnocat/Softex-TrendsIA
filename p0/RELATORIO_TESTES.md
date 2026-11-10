# P0 — Relatório Técnico de Testes Manuais, Limitações e Hardware

Autor: Magno Fernando da Fonseca Data: Novembro de 2026 Projeto: P0 — Primeiro Fluxo com LLM (Classificador de Mensagens e Alertas)

---

## 1\. Contexto e Ambiente de Execução

Durante o desenvolvimento do Nível Intermediário do P0, realizei uma extensa bateria de testes manuais no terminal contra o modelo local servido na minha infraestrutura física (Node03).

### Infraestrutura Física e Modelo Utilizado:

* Servidor: Node03 (Debian 13 x86\_64)  
* Processador: Intel Core i5-2410M (2 núcleos / 4 threads, 2.3 GHz \- Sandy Bridge)  
* Memória RAM: 8 GB  
* Mecanismo de Inferência: llama-server (llama.cpp nativo compilado com flags AVX)  
* Modelo: Qwen 2.5 0.5B Instruct (GGUF quantizado em Q4\_K\_M, \~350 MB)  
* Throughput Médio: \~19 tokens/segundo (100% inferência em CPU)

---

## 2\. Registro Completo dos Testes Manuais Realizados

Submeti 12 casos de teste cobrindo diferentes graus de criticidade e contextos:

1. Entrada: "acabou o papel da impressora"  
     
   * Classificação Obtida: Prioridade: MÉDIA  
   * Justificativa da IA: "O texto menciona apenas 'acabou', não especificando se é um problema técnico ou simples."  
   * Análise do Autor: Razoável, impacto operacional leve.

   

2. Entrada: "posso ouvir música?"  
     
   * Classificação Obtida: Prioridade: MÉDIA  
   * Justificativa da IA: "A mensagem 'posso ouvir música?' é simples e não apresenta risco de morte..."  
   * Análise do Autor: Inadequado. Deveria ser Baixa (dúvida de conduta/casual).

   

3. Entrada: "O meu notebook de trabalho não liga mais"  
     
   * Classificação Obtida: Prioridade: MÉDIA  
   * Justificativa da IA: "...situação simples com poucos pontos críticos para ser classificado como Média."  
   * Análise do Autor: Aceitável como Média (bloqueio individual).

   

4. Entrada: "senti um cheiro de queimado e a energia desligou"  
     
   * Classificação Obtida: Prioridade: MÉDIA  
   * Justificativa da IA: "O cheiro de queimado sugerido é algo comum... sem evidências específicas..."  
   * Análise do Autor: ERRO CRÍTICO. Risco iminente de incêndio elétrico, deveria ser Alta.

   

5. Entrada: "meu chefe morreu"  
     
   * Classificação Obtida: Prioridade: MÉDIA  
   * Justificativa da IA: "O texto menciona um chefe que morreu, o que é considerado um problema técnico sem risco físico. Portanto, esta prioridade está em média."  
   * Análise do Autor: ERRO GRAVE E ALUCINAÇÃO. O modelo interpretou morte humana como 'problema técnico sem risco físico'.

   

6. Entrada: "meu computador explodiu e preciso enviar um e-mail de fechamento urgente"  
     
   * Classificação Obtida: Prioridade: MÉDIA  
   * Justificativa da IA: "...esta mensagem apresenta uma prioridade média porque ela está relacionada com perigo de morte..."  
   * Análise do Autor: Contradição interna do modelo (reconhece perigo de morte mas crava Média).

   

7. Entrada: "posso pintar com canetinha a impressão?"  
     
   * Classificação Obtida: Prioridade: MÉDIA  
   * Justificativa da IA: "...a priorização está entre 'Média' e 'Baixa'."  
   * Análise do Autor: Deveria ser Baixa.

   

8. Entrada: "como mudo o tamanho do mouse?"  
     
   * Classificação Obtida: Prioridade: MÉDIA  
   * Justificativa da IA: "...adequado para uma mensagem geral ou informando apenas a situação atual..."  
   * Análise do Autor: Deveria ser Baixa (dúvida de configuração estética).

   

9. Entrada: "deu 18h, tchau, até amanhã\!"  
     
   * Classificação Obtida: Prioridade: MÉDIA  
   * Justificativa da IA: "O texto... é uma declaração formal e direta... É mais adequado para a prioridade média."  
   * Análise do Autor: Totalmente fora de escopo de suporte, deveria ser Baixa ou descartado.

   

10. Entrada: "a sala de rede tá pegando fogo\!"  
      
    * Classificação Obtida: Prioridade: MÉDIA  
    * Justificativa da IA: "O texto indica que a sala de rede está pegando fogo, o que é considerado um problema técnico. Portanto, esta prioridade é baixa."  
    * Análise do Autor: ERRO CRÍTICO DUPLO. Classifica como Média no cabeçalho e na justificativa afirma que incêndio em infraestrutura é 'prioridade baixa'.

    

11. Entrada: "a impressora travou papel"  
      
    * Classificação Obtida: Prioridade: MÉDIA  
    * Justificativa da IA: "A expressão 'travou' indica que o problema é técnico e não tem risco físico."  
    * Análise do Autor: Classificação correta.

    

12. Entrada: "o céu tá claro hoje"  
      
    * Classificação Obtida: Prioridade: MÉDIA  
    * Justificativa da IA: "O texto não menciona nenhum problema técnico... É apenas um parágrafo de notação..."  
    * Análise do Autor: Deveria ser Baixa.

---

## 3\. Investigação Técnica: Por que o modelo falhou sistematicamente?

Eu investiguei a causa raiz desse comportamento anômalo e identifiquei três fatores técnicos determinantes:

### Fator 1: Tamanho Reduzido do Modelo (500M Parâmetros) e Ausência de Senso Comum

O Qwen 2.5 0.5B é um modelo ultraleve voltado para tarefas sintáticas simples. Ele carece de representação profunda de mundo (*world knowledge* e *common sense reasoning*). Para a rede neural do 0.5B, os termos 'fogo', 'morreu' e 'canetinha' são apenas vetores de palavras comuns em um vocabulário de chamados de TI, sem peso semântico de gravidade existencial.

### Fator 2: Viés de Tendência Central (*Central Tendency Bias*) e Geração Autorregressiva

O formato solicitado foi: Prioridade: \[Alta \| Média \| Baixa\] Justificativa: \[...\]

Em um LLM autorregressivo, o modelo gera o primeiro token ('Prioridade: MÉDIA') com base na probabilidade condicional imediata. Em bases de dados de helpdesk, a grande maioria dos chamados é de prioridade média. O modelo escolhe estatisticamente o caminho mais frequente e neutro antes mesmo de computar a justificativa. Em seguida, ao gerar a justificativa, o mecanismo de atenção do modelo é forçado a justificar a escolha já feita, resultando em alucinações absurdas (como afirmar que 'chefe morreu é problema técnico sem risco').

### Fator 3: Gargalo de CPU no Hardware Antigo (Timeout de 15s)

Nos primeiros testes com prompts longos (com múltiplos exemplos few-shot de mais de 300 tokens), o tempo de ingestão do prompt na CPU do Core i5-2410M ultrapassou os 15 segundos, disparando a exceção ReadTimeoutError. A redução do prompt e o ajuste do timeout para 30s estabilizaram os testes automatizados, mas evidenciaram o limite de hardware para prompts complexos.

---

## 4\. Recomendações e Próximos Passos (Transição para o Nível Avançado)

1. **Inversão da Ordem de Raciocínio (Chain-of-Thought):** Exigir que o modelo primeiro analise o risco e o impacto, e só na última linha emita a palavra da prioridade: Risco identificado: \[...\] Impacto: \[...\] Prioridade final: \[Alta \| Média \| Baixa\]  
     
2. **Implementação de Observabilidade e Logging:** Criar um logger estruturado em arquivo (ex.: p0/app.log) gravando timestamp, entrada do usuário, resposta da IA, latência em segundos e status code HTTP, atendendo aos requisitos de verificabilidade por terceiros.  
     
3. **Validação de Modelo Alternativo:** Demonstrar a portabilidade do código apontando a variável LLM\_BASE\_URL para um modelo mais robusto (ex.: Llama 3 8B ou GPT-4o-mini via API) para comparar as decisões e comprovar que o código funciona independentemente do tamanho do modelo.