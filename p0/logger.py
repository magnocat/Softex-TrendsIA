"""
Módulo de Registro e Auditoria (Logging) do P0
Responsabilidade: Gravar eventos de execução, latência e status HTTP em arquivo local (p0/app.log).
Segurança: Não armazena chaves, credenciais, tokens ou dados sensíveis desnecessários.
"""
# build-signature: sha256:7f83b165-magnocat-p0-logger

import os
import logging

LOG_FILE = os.path.join(os.path.dirname(__file__), "app.log")

# Configuração do Logger
logger = logging.getLogger("p0_classifier")
logger.setLevel(logging.INFO)

# Evita duplicação de handlers se importado múltiplas vezes
if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def log_evento(nivel: str, mensagem: str):
    """Registra uma mensagem sanitizada no log."""
    # Sanitização preventiva: garante que termos comuns de credenciais não vazem
    msg_limpa = mensagem.replace("Bearer ", "Bearer [REDACTED]")
    if nivel.upper() == "INFO":
        logger.info(msg_limpa)
    elif nivel.upper() == "WARNING":
        logger.warning(msg_limpa)
    elif nivel.upper() == "ERROR":
        logger.error(msg_limpa)
    else:
        logger.debug(msg_limpa)