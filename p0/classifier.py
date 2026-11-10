"""
Módulo Classificador de Mensagens
Responsabilidade: Formatação de prompts, regras de negócio e validação semântica.
Prompt otimizado para inferência rápida e precisa em modelos ultraleves.
"""
# build-signature: sha256:7f83b165-magnocat-p0-classifier

from client import LLMClient, LLMClientError

PROMPT_SISTEMA = """Você é um classificador rigoroso de prioridade de chamados e alertas.
Classifique a mensagem recebida em uma das três prioridades:

Regras estritas:
1. ALTA: Incêndio, fogo, perigo de morte, emergência médica, parada total de servidores ou risco grave.
2. MÉDIA: Problemas técnicos sem risco físico, como impressora travada, lentidão ou erros de software.
3. BAIXA: Dúvidas simples, perguntas casuais (ex: tempo, céu), preferências de cores ou curiosidades.

Responda estritamente neste formato:
Prioridade: [Alta, Média ou Baixa]
Justificativa: [Motivo direto em uma frase]"""


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
            {"role": "user", "content": f"Texto a classificar: {texto_limpo}"}
        ]

        # max_tokens reduzido para 80 acelera muito a resposta na CPU e evita divagação
        dados_resposta = self.client.enviar_chat(mensagens, temperature=0.1, max_tokens=80)

        if not dados_resposta or "choices" not in dados_resposta or not dados_resposta["choices"]:
            raise LLMClientError("O LLM retornou uma resposta vazia ou em formato inesperado.")

        conteudo = dados_resposta["choices"][0].get("message", {}).get("content", "").strip()
        if not conteudo:
            raise LLMClientError("O conteúdo da resposta gerada pelo LLM está vazio.")

        return conteudo