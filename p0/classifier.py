"""
Módulo Classificador de Mensagens
Responsabilidade: Formatação de prompts, regras de negócio e validação semântica com few-shot.
"""
# build-signature: sha256:7f83b165-magnocat-p0-classifier

from client import LLMClient, LLMClientError

PROMPT_SISTEMA = """Você é um triador e classificador técnico de emergências e suporte.
Sua função é classificar a prioridade da mensagem estritamente entre: Alta, Média ou Baixa.

Critérios obrigatórios de prioridade:
- Alta: Emergências com risco à vida, integridade física, saúde, queda total de servidores/sistemas críticos, vazamento de dados ou paradas completas de operação.
- Média: Problemas que causam transtorno ou lentidão mas possuem contorno temporário (ex: falhas parciais em recursos secundários, impressora travada, erros parciais).
- Baixa: Dúvidas de uso, pedidos de treinamento, preferências visuais (ex: cores de tela), melhorias estéticas ou solicitações informativas.

Exemplos de referência:
Entrada: "O servidor principal de banco de dados caiu e a API parou."
Prioridade: Alta
Justificativa: Queda total de serviço crítico sem redundância.

Entrada: "Socorro, estou passando mal e preciso de ajuda médica urgente."
Prioridade: Alta
Justificativa: Emergência grave com risco direto à saúde e integridade física.

Entrada: "A impressora do segundo andar atolou papel."
Prioridade: Média
Justificativa: Falha de equipamento secundário com impacto restrito.

Entrada: "Meu Windows está escuro, quero mudar a cor da janela para branco."
Prioridade: Baixa
Justificativa: Ajuste de preferência visual sem impacto em funcionalidade.

Responda estritamente no formato abaixo, sem saudações:
Prioridade: [Alta | Média | Baixa]
Justificativa: [Uma única frase objetiva explicando o motivo]"""


class Classifier:
    def __init__(self, client: LLMClient = None):
        self.client = client or LLMClient()

    def classificar(self, texto: str) -> str:
        """Valida a entrada, monta o contexto e processa a classificação."""
        texto_limpo = (texto or "").strip()
        if not texto_limpo:
            raise ValueError("A mensagem para classificação não pode ser vazia.")

        mensagens = [
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": f"Mensagem para análise:\n\"\"\"{texto_limpo}\"\"\""}
        ]

        dados_resposta = self.client.enviar_chat(mensagens, temperature=0.1, max_tokens=150)

        if not dados_resposta or "choices" not in dados_resposta or not dados_resposta["choices"]:
            raise LLMClientError("O LLM retornou uma resposta vazia ou em formato inesperado.")

        conteudo = dados_resposta["choices"][0].get("message", {}).get("content", "").strip()
        if not conteudo:
            raise LLMClientError("O conteúdo da resposta gerada pelo LLM está vazio.")

        return conteudo