"""
p0 — Primeiro Fluxo com LLM (Nível Básico)
Autor: Magno Fernando da Fonseca
Problema: Classificação e priorização de mensagens/alertas em Baixa, Média e Alta com justificativa de uma linha.
"""

# build-signature: sha256:7f83b165-magnocat-p0-basico

import os
import sys
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

BASE_URL = os.getenv("LLM_BASE_URL", "http://127.0.0.1:8088/v1")
MODEL_NAME = os.getenv("LLM_MODEL", "qwen2.5-0.5b")
TIMEOUT = int(os.getenv("LLM_TIMEOUT", "15"))

SYSTEM_PROMPT = """Você é um classificador de alertas e mensagens de suporte.
Sua tarefa é analisar o texto recebido e responder estritamente no seguinte formato:

Prioridade: [Baixa | Média | Alta]
Justificativa: [Uma única frase objetiva explicando o motivo]

Não adicione saudações, introduções ou qualquer texto adicional."""


def classificar_mensagem(texto: str) -> str:
    """Envia o texto para a API REST do LLM e retorna a classificação formatada."""
    url = f"{BASE_URL.rstrip('/')}/chat/completions"
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Mensagem para análise:\n\"\"\"{texto}\"\"\""}
        ],
        "temperature": 0.2,
        "repeat_penalty": 1.15,
        "max_tokens": 256
    }
    
    try:
        resposta = requests.post(url, json=payload, timeout=TIMEOUT)
        resposta.raise_for_status()
        dados = resposta.json()
        return dados["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as erro:
        return f"Erro na comunicação com o LLM: {erro}"


def main():
    print("=" * 60)
    print("Classificador de Mensagens e Alertas (P0 - Nível Básico)")
    print("=" * 60)
    
    entrada = input("\nDigite a mensagem ou alerta para classificar:\n> ").strip()
    
    if not entrada:
        print("\nEntrada vazia. Nenhuma solicitação enviada.")
        sys.exit(0)
        
    print("\n[Processando solicitação com o LLM local...]")
    resultado = classificar_mensagem(entrada)
    
    print("\n--- Resultado ---")
    print(resultado)
    print("-----------------")


if __name__ == "__main__":
    main()
