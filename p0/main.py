"""
P0 — Primeiro Fluxo com LLM (Nível Intermediário Aprimorado)
Autor: Magno Fernando da Fonseca
Orquestrador principal da aplicação com tratamento de erros HTTP granulares (401, 409, 429, timeout e conexão).
"""
# build-signature: sha256:7f83b165-magnocat-p0-main

import sys
from config import Config
from client import (
    LLMClient,
    LLMAuthenticationError,
    LLMUnavailableError,
    LLMTimeoutError,
    LLMRateLimitError,
    LLMConflictError,
    LLMClientError
)
from classifier import Classifier


def capturar_entrada() -> str:
    """Captura e sanitiza a entrada textual via terminal."""
    try:
        entrada = input("\nDigite a mensagem ou alerta para classificar:\n> ")
        return entrada.strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\nOperação cancelada pelo usuário.")
        sys.exit(0)


def exibir_resultado(resultado: str):
    """Apresenta a classificação de maneira formatada."""
    print("\n" + "=" * 50)
    print("           RESULTADO DA CLASSIFICAÇÃO")
    print("=" * 50)
    print(resultado)
    print("=" * 50 + "\n")


def exibir_erro(titulo: str, detalhe: str):
    """Apresenta mensagens de erro amigáveis sem expor stacktraces ao usuário."""
    print("\n" + "!" * 50)
    print(f"[FALHA NA OPERAÇÃO] {titulo}")
    print(f"Detalhe: {detalhe}")
    print("!" * 50 + "\n")


def main():
    print("=" * 60)
    print("Classificador de Mensagens e Alertas (P0 - Nível Intermediário)")
    print("=" * 60)

    try:
        Config.validar()
    except ValueError as e:
        exibir_erro("Configuração Inválida", str(e))
        sys.exit(1)

    mensagem = capturar_entrada()
    if not mensagem:
        exibir_erro("Entrada Rejeitada", "O texto informado está vazio. Forneça uma mensagem válida.")
        sys.exit(1)

    classificador = Classifier()
    try:
        print("\n[Enviando solicitação ao modelo de linguagem...]")
        resultado = classificador.classificar(mensagem)
        exibir_resultado(resultado)

    except LLMAuthenticationError as e:
        exibir_erro("Autenticação Recusada", str(e))
        sys.exit(2)
    except LLMRateLimitError as e:
        exibir_erro("Limite de Cota Excedido (429)", str(e))
        sys.exit(3)
    except LLMConflictError as e:
        exibir_erro("Conflito na Requisição (409)", str(e))
        sys.exit(4)
    except LLMUnavailableError as e:
        exibir_erro("Serviço Indisponível", str(e))
        sys.exit(5)
    except LLMTimeoutError as e:
        exibir_erro("Tempo Limite Esgotado", str(e))
        sys.exit(6)
    except (LLMClientError, ValueError) as e:
        exibir_erro("Processamento Interrompido", str(e))
        sys.exit(7)
    except Exception as e:
        exibir_erro("Erro Não Mapeado", f"Ocorreu uma falha imprevista: {str(e)}")
        sys.exit(99)


if __name__ == "__main__":
    main()