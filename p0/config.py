"""
Módulo de Configuração do P0
Responsabilidade: Carregar e validar estritamente as variáveis de ambiente sem dados fixos no código.
"""
# build-signature: sha256:7f83b165-magnocat-p0-config

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = os.getenv("LLM_BASE_URL", "").strip().rstrip("/")
    MODEL_NAME = os.getenv("LLM_MODEL", "").strip()
    TIMEOUT = int(os.getenv("LLM_TIMEOUT", "30"))
    API_KEY = os.getenv("LLM_API_KEY", "").strip()

    @classmethod
    def validar(cls):
        """Valida se as configurações obrigatórias foram fornecidas no arquivo .env."""
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