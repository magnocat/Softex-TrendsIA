"""
Módulo Cliente de Comunicação REST (Nível Avançado - Corrigido)
Responsabilidade: Preparar requisição, controlar headers/autenticação, medir latência e registrar auditoria via log.
Compatibilidade: Aceita parâmetros dinâmicos da Config e permite overrides opcionais de temperatura e tokens.
"""
# build-signature: sha256:7f83b165-magnocat-p0-client-v4

import time
import requests
from config import Config
from logger import log_evento


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

    def preparar_payload(self, mensagens: list, temperature: float = None, max_tokens: int = None) -> dict:
        """Monta o payload da requisição com parâmetros dinâmicos ou overrides."""
        temp = temperature if temperature is not None else self.config.TEMPERATURE
        tokens = max_tokens if max_tokens is not None else self.config.MAX_TOKENS
        return {
            "model": self.config.MODEL_NAME,
            "messages": mensagens,
            "temperature": temp,
            "repeat_penalty": self.config.REPEAT_PENALTY,
            "max_tokens": tokens
        }

    def enviar_chat(self, mensagens: list, temperature: float = None, max_tokens: int = None) -> dict:
        """Executa a requisição REST contra o endpoint /chat/completions registrando auditoria."""
        self.config.validar()
        url = f"{self.config.BASE_URL}/chat/completions"

        headers = {"Content-Type": "application/json"}
        if self.config.API_KEY:
            headers["Authorization"] = f"Bearer {self.config.API_KEY}"

        payload = self.preparar_payload(mensagens, temperature=temperature, max_tokens=max_tokens)

        log_evento("INFO", f"Enviando requisicao REST para {self.config.BASE_URL} (modelo: {self.config.MODEL_NAME})")
        inicio = time.perf_counter()

        try:
            resposta = requests.post(url, json=payload, headers=headers, timeout=self.config.TIMEOUT)
            duracao = time.perf_counter() - inicio

            if resposta.status_code in (401, 403):
                log_evento("ERROR", f"Falha de autenticacao HTTP {resposta.status_code} em {duracao:.2f}s")
                raise LLMAuthenticationError(
                    "Credencial ausente ou inválida. Verifique o valor de LLM_API_KEY no arquivo .env."
                )

            if resposta.status_code == 429:
                log_evento("WARNING", f"Cota ou limite de taxa excedido HTTP 429 em {duracao:.2f}s")
                raise LLMRateLimitError(
                    "Limite de cota ou taxa de requisições excedido no provedor de LLM (HTTP 429). Aguarde alguns instantes."
                )

            if resposta.status_code == 409:
                log_evento("WARNING", f"Conflito de estado HTTP 409 em {duracao:.2f}s")
                raise LLMConflictError(
                    "Conflito de estado na solicitação enviada ao LLM (HTTP 409). Verifique os parâmetros da requisição."
                )

            if resposta.status_code in (502, 503, 504):
                log_evento("ERROR", f"Servico indisponivel HTTP {resposta.status_code} em {duracao:.2f}s")
                raise LLMUnavailableError(
                    f"O serviço de LLM está temporariamente indisponível (HTTP {resposta.status_code})."
                )

            resposta.raise_for_status()
            log_evento("INFO", f"Requisicao concluida com sucesso em {duracao:.2f}s (HTTP {resposta.status_code})")
            return resposta.json()

        except requests.exceptions.Timeout:
            duracao = time.perf_counter() - inicio
            log_evento("ERROR", f"Timeout de {self.config.TIMEOUT}s atingido apos {duracao:.2f}s")
            raise LLMTimeoutError(
                f"Tempo limite ({self.config.TIMEOUT}s) excedido ao aguardar resposta do LLM."
            )
        except requests.exceptions.ConnectionError:
            log_evento("ERROR", f"Falha de conexao com endpoint {self.config.BASE_URL}")
            raise LLMUnavailableError(
                f"Falha de conexão com '{self.config.BASE_URL}'. Verifique se o servidor de LLM está ativo."
            )
        except requests.exceptions.RequestException as e:
            log_evento("ERROR", f"Erro inesperado na chamada REST: {str(e)}")
            raise LLMClientError(f"Erro inesperado na chamada REST: {str(e)}")