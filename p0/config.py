"""
Módulo de Configuração do P0 (Nível Avançado)
Responsabilidade: Carregar, validar e fornecer parâmetros de acesso e de geração do LLM.
Permite alterar temperatura, limite de tokens e penalidade sem tocar no código principal.
"""
# build-signature: sha256:7f83b165-magnocat-p0-config-v3

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Acesso e Conectividade
    BASE_URL = os.getenv("LLM_BASE_URL", "").strip().rstrip("/")
    MODEL_NAME = os.getenv("LLM_MODEL", "").strip()
    TIMEOUT = int(os.getenv("LLM_TIMEOUT", "30"))
    API_KEY = os.getenv("LLM_API_KEY", "").strip()

    # Parâmetros de Geração (Configuráveis sem alterar o código)
    TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "100"))
    REPEAT_PENALTY = float(os.getenv("LLM_REPEAT_PENALTY", "1.15"))

    @classmethod
    def validar(cls):
        """Valida se as configurações obrigatórias e limites numéricos são consistentes."""
        if not cls.BASE_URL:
            raise ValueError(
                "A variável de ambiente LLM_BASE_URL não está configurada no seu arquivo .env. "
                "Consulte o arquivo p0/.env.example para preencher a URL de acesso ao LLM."
            )
        if not cls.BASE_URL.startswith("http://") and not cls.BASE_URL.startswith("https://"):
            raise ValueError(
                f"URL base inválida: '{cls.BASE_URL}'. O endereço deve iniciar com http:// ou https://."
            )
        if not cls.MODEL_NAME:
            raise ValueError(
                "A variável de ambiente LLM_MODEL não está configurada no seu arquivo .env. "
                "Informe o identificador do modelo (ex.: qwen2.5-0.5b)."
            )
        if cls.TIMEOUT <= 0:
            raise ValueError("A variável LLM_TIMEOUT deve ser um número inteiro positivo.")
        if not (0.0 <= cls.TEMPERATURE <= 2.0):
            raise ValueError("A variável LLM_TEMPERATURE deve estar entre 0.0 e 2.0.")
        if cls.MAX_TOKENS <= 0:
            raise ValueError("A variável LLM_MAX_TOKENS deve ser maior que zero.")
        if cls.REPEAT_PENALTY <= 0:
            raise ValueError("A variável LLM_REPEAT_PENALTY deve ser maior que zero.")