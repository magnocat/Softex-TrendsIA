"""
Módulo Classificador de Mensagens
Responsabilidade: Classificação com raciocínio prévio (Chain-of-Thought invertido).
Técnica: Força o modelo a avaliar o risco e o impacto ANTES de emitir a palavra da prioridade.
"""
# build-signature: sha256:7f83b165-magnocat-p0-classifier-cot

from client import LLMClient, LLMClientError

PROMPT_SISTEMA = """Você é um assistente de triagem de incidentes de TI e emergências.
Analise a mensagem do usuário passo a passo, preenchendo obrigatoriamente os três campos abaixo na ordem exata:

1. Risco grave (vida, saúde, fogo, queda total de servidor): [Sim ou Não]
2. Tipo do chamado: [Emergência | Falha técnica comum | Dúvida ou Casual]
3. Prioridade: [Se houver risco grave, responda Alta. Se for falha comum sem risco, responda Média. Se for dúvida ou casual, responda Baixa.]

Formato estrito de resposta:
Risco grave: [Sim | Não]
Tipo: [Emergência | Falha técnica | Dúvida]
Prioridade: [Alta | Média | Baixa]
Justificativa: [Uma frase curta]"""


class Classifier:
    def __init__(self, client: LLMClient = None):
        self.client = client or LLMClient()

    def classificar(self, texto: str) -> str:
        """Valida a entrada, monta o contexto e processa a classificação com Chain-of-Thought."""
        texto_limpo = (texto or "").strip()
        if not texto_limpo:
            raise ValueError("A mensagem para classificação não pode ser vazia.")

        mensagens = [
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": f"Mensagem a analisar: \"{texto_limpo}\""}
        ]

        dados_resposta = self.client.enviar_chat(mensagens, temperature=0.1, max_tokens=100)

        if not dados_resposta or "choices" not in dados_resposta or not dados_resposta["choices"]:
            raise LLMClientError("O LLM retornou uma resposta vazia ou em formato inesperado.")

        conteudo = dados_resposta["choices"][0].get("message", {}).get("content", "").strip()
        if not conteudo:
            raise LLMClientError("O conteúdo da resposta gerada pelo LLM está vazio.")

        return conteudo