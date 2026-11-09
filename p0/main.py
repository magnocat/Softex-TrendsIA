"""
p0 — Primeiro Fluxo com LLM (Nível Básico aprimorado)
Autor: Magno Fernando da Fonseca
Problema: Classificação e priorização de mensagens/alertas em Baixa, Média e Alta com justificativa de uma linha.
Suporte universal: LLM local (Node03) e provedores em nuvem via API Key.
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
API_KEY = os.getenv("LLM_API_KEY", "").strip()

SYSTEM_PROMPT = """Você é um classificador de alertas e mensagens de suporte.
Sua tarefa é analisar o texto recebido e responder estritamente no seguinte formato:

Prioridade: [Baixa | Média | Alta]
Justificativa: [Uma única frase objetiva explicando o motivo]

Não adicione saudações, introduções ou qualquer texto adicional."""


def classificar_mensagem(texto: str) -> str:
    """Envia o texto para a API REST do LLM e retorna a classificação formatada."""
    url = f"{BASE_URL.rstrip('/')}/chat/completions"

    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"

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
        resposta = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)

        if resposta.status_code == 401:
            return "Erro 401 (Não autorizado): A API exigiu autenticação. Verifique se a variável LLM_API_KEY está configurada no seu arquivo .env."

        resposta.raise_for_status()
        dados = resposta.json()
        return dados["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        return f"Erro de Timeout: O LLM em {BASE_URL} não respondeu dentro do limite de {TIMEOUT} segundos."
    except requests.exceptions.ConnectionError:
        return f"Erro de Conexão: Não foi possível conectar ao endpoint {BASE_URL}. Verifique se o serviço está ativo na porta informada."
    except requests.exceptions.RequestException as erro:
        return f"Erro na requisição REST: {erro}"


def main():
    print("=" * 60)
    print("Classificador de Mensagens e Alertas (P0 - Nível Básico)")
    print("=" * 60)

    entrada = input("\nDigite a mensagem ou alerta para classificar:\n> ").strip()

    if not entrada:
        print("\nEntrada vazia. Nenhuma solicitação enviada.")
        sys.exit(0)

    print("\n[Processando solicitação com o LLM...]")
    resultado = classificar_mensagem(entrada)

    print("\n--- Resultado ---")
    print(resultado)
    print("-----------------")


if __name__ == "__main__":
    main()