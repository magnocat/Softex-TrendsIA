"""
Módulo Cliente de Comunicação REST
Responsabilidade: Preparar requisição, controlar headers/autenticação e tratar falhas de transporte e limites.
"""
# build-signature: sha256:7f83b165-magnocat-p0-client

import requests
from config import Config


class LLMClientError(Exception):
    """Exceção base para falhas na comunicação com o LLM."""
    pass


class LLMAuthenticationError(LLMClientError):
    """Falha de autenticação (credencial ausente ou inválida - HTTP 401/403)."""
    pass


class LLMUnavailableError(LLMClientError):
    """Serviço indisponível ou inacessível (Connection Error, 502, 503)."""
    pass


class LLMTimeoutError(LLMClientError):
    """Tempo limite de resposta esgotado."""
    pass


class LLMRateLimitError(LLMClientError):
    """Limite de requisições ou cota do LLM excedida (HTTP 429)."""
    pass


class LLMConflictError(LLMClientError):
    """Conflito na solicitação ao LLM (HTTP 409)."""
    pass


class LLMClient:
    def __init__(self, config: Config = Config):
        self.config = config

    def enviar_chat(self, mensagens: list, temperature: float = 0.1, max_tokens: int = 150) -> dict:
        """Executa a requisição REST contra o endpoint /chat/completions."""
        self.config.validar()
        url = f"{self.config.BASE_URL}/chat/completions"

        headers = {"Content-Type": "application/json"}
        if self.config.API_KEY:
            headers["Authorization"] = f"Bearer {self.config.API_KEY}"

        payload = {
            "model": self.config.MODEL_NAME,
            "messages": mensagens,
            "temperature": temperature,
            "repeat_penalty": 1.15,
            "max_tokens": max_tokens
        }

        try:
            resposta = requests.post(url, json=payload, headers=headers, timeout=self.config.TIMEOUT)

            if resposta.status_code in (401, 403):
                raise LLMAuthenticationError(
                    "Credencial ausente ou inválida. Verifique o valor de LLM_API_KEY no arquivo .env."
                )

            if resposta.status_code == 429:
                raise LLMRateLimitError(
                    "Limite de cota ou taxa de requisições excedido no provedor de LLM (HTTP 429). Aguarde alguns instantes."
                )

            if resposta.status_code == 409:
                raise LLMConflictError(
                    "Conflito de estado na solicitação enviada ao LLM (HTTP 409). Verifique os parâmetros da requisição."
                )

            if resposta.status_code in (502, 503, 504):
                raise LLMUnavailableError(
                    f"O serviço de LLM está temporariamente indisponível (HTTP {resposta.status_code})."
                )

            resposta.raise_for_status()
            return resposta.json()

        except requests.exceptions.Timeout:
            raise LLMTimeoutError(
                f"Tempo limite ({self.config.TIMEOUT}s) excedido ao aguardar resposta do LLM."
            )
        except requests.exceptions.ConnectionError:
            raise LLMUnavailableError(
                f"Falha de conexão com '{self.config.BASE_URL}'. Verifique se o servidor de LLM está ativo."
            )
        except requests.exceptions.RequestException as e:
            raise LLMClientError(f"Erro inesperado na chamada REST: {str(e)}")