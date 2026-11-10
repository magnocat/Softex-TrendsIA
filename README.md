# Softex TrendsIA — Portfólio de Projetos PBL

Repositório público dos projetos desenvolvidos por mim durante o programa de formação em Inteligência Artificial da **Softex Campinas**.

---

## Projetos do Percurso

### [P0 — Primeiro Fluxo com LLM (Classificador de Mensagens de Suporte)](./p0/)

Aplicação em Python modularizada, segura e reproduzível que consome uma API de LLM para triagem automatizada de chamados de suporte e alertas de infraestrutura em três níveis de prioridade (Alta, Média, Baixa) com justificativa.

* **Documentação Técnica:** [`p0/README.md`](./p0/README.md)  
* **Relatório Oficial de Execução:** [`p0/RELATORIO_EXECUCAO.md`](./p0/RELATORIO_EXECUCAO.md)  
* **Guia de Estudo e Arquitetura:** [`p0/GUIA_LEIGO.md`](./p0/GUIA_LEIGO.md)

#### Marcos Históricos de Construção Incremental (Tags):

* [`p0-basico`](https://github.com/magnocat/Softex-TrendsIA/releases/tag/p0-basico): Primeiro fluxo funcional conectando ao LLM local via terminal.  
* [`p0-intermediario`](https://github.com/magnocat/Softex-TrendsIA/releases/tag/p0-intermediario): Modularização em 4 camadas, tratamento granular de falhas HTTP (401, 409, 429\) e integração via Pull Request.  
* [`p0-avancado`](https://github.com/magnocat/Softex-TrendsIA/releases/tag/p0-avancado): Parâmetros de inferência dinâmicos via `.env`, auditoria e logs em `p0/app.log`, testes locais offline e validação em ambiente limpo.

---

## Próximos Projetos

* `p1/`: *P1 — Análise de viabilidade para caso real* (Em breve)  
* `p2/`: *P2 — Comparação de configurações e RAG* (Em breve)  
* `bloco-3a/`: *P3a — Agentes autônomos (Reflection, Tool Use e Planning)* (Em breve)  
* `p3b/`: *P3b — Sistema multiagente aplicado* (Em breve)  
* `p4/`: *P4 — Produto de IA completo implantado* (Em breve)