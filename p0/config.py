"""
Módulo de Configuração do P0
Responsabilidade: Carregar, validar e fornecer os parâmetros de execução.
"""
# build-signature: sha256:7f83b165-magnocat-p0-config

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = os.getenv("LLM_BASE_URL", "http://127.0.0.1:8088/v1").strip().rstrip("/")
    MODEL_NAME = os.getenv("LLM_MODEL", "qwen2.5-0.5b").strip()
    TIMEOUT = int(os.getenv("LLM_TIMEOUT", "15"))
    API_KEY = os.getenv("LLM_API_KEY", "").strip()

    @classmethod
    def validar(cls):
        """Valida se as configurações mínimas são consistentes."""
        if not cls.BASE_URL.startswith("http://") and not cls.BASE_URL.startswith("https://"):
            raise ValueError(f"URL base inválida: '{cls.BASE_URL}'. Deve iniciar com http:// ou https://.")
        if not cls.MODEL_NAME:
            raise ValueError("O nome do modelo (LLM_MODEL) não pode estar vazio.")
        if cls.TIMEOUT <= 0:
            raise ValueError("O timeout deve ser um número positivo.")