"""
Módulo Classificador de Mensagens
Responsabilidade: Formatação de prompts, validação semântica e tratamento da resposta.
"""
# build-signature: sha256:7f83b165-magnocat-p0-classifier

from client import LLMClient, LLMClientError

PROMPT_SISTEMA = """Você é um classificador de alertas e mensagens de suporte.
Analise a mensagem e responda estritamente no formato:

Prioridade: [Baixa | Média | Alta]
Justificativa: [Uma única frase objetiva explicando o motivo]

Não adicione saudações ou explicações extras."""


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

        dados_resposta = self.client.enviar_chat(mensagens)

        # Validação do formato recebido
        if not dados_resposta or "choices" not in dados_resposta or not dados_resposta["choices"]:
            raise LLMClientError("O LLM retornou uma resposta vazia ou em formato inesperado.")

        conteudo = dados_resposta["choices"][0].get("message", {}).get("content", "").strip()
        if not conteudo:
            raise LLMClientError("O conteúdo da resposta gerada pelo LLM está vazio.")

        return conteudo