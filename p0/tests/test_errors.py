"""
Bateria de Testes do P0 — Casos Reais e Simulados (Mocks)
Demonstração de resiliência e tratamento de falhas previsíveis.
"""
# build-signature: sha256:7f83b165-magnocat-p0-tests

import unittest
from unittest.mock import patch, Mock
import requests

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import Config
from client import (
    LLMClient,
    LLMAuthenticationError,
    LLMUnavailableError,
    LLMTimeoutError,
    LLMClientError
)
from classifier import Classifier


class TestP0TratamentoDeErros(unittest.TestCase):

    def setUp(self):
        self.client = LLMClient()
        self.classifier = Classifier(self.client)

    # 1. Validação de Entrada
    def test_rejeicao_entrada_vazia(self):
        """Garante que entradas vazias ou espaços são impedidas antes de chamar o LLM."""
        with self.assertRaises(ValueError):
            self.classifier.classificar("   ")

    # 2. Teste Simulado: Credencial Inválida (HTTP 401)
    @patch("requests.post")
    def test_simulado_credencial_invalida_401(self, mock_post):
        """Simula resposta HTTP 401 para demonstrar tratamento de credencial inválida."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        with self.assertRaises(LLMAuthenticationError) as contexto:
            self.client.enviar_chat([{"role": "user", "content": "teste"}])
        self.assertIn("Credencial ausente ou inválida", str(contexto.exception))

    # 3. Teste Simulado: Serviço Indisponível (ConnectionError)
    @patch("requests.post")
    def test_simulado_servico_indisponivel(self, mock_post):
        """Simula queda de rede ou serviço desligado."""
        mock_post.side_effect = requests.exceptions.ConnectionError("Conexão recusada")

        with self.assertRaises(LLMUnavailableError) as contexto:
            self.client.enviar_chat([{"role": "user", "content": "teste"}])
        self.assertIn("Falha de conexão", str(contexto.exception))

    # 4. Teste Simulado: Timeout de Resposta
    @patch("requests.post")
    def test_simulado_timeout(self, mock_post):
        """Simula estouro do tempo limite configurado."""
        mock_post.side_effect = requests.exceptions.Timeout("Timeout atingido")

        with self.assertRaises(LLMTimeoutError) as contexto:
            self.client.enviar_chat([{"role": "user", "content": "teste"}])
        self.assertIn("Tempo limite", str(contexto.exception))

    # 5. Teste Simulado: Resposta em formato inesperado / JSON malformado
    @patch("requests.post")
    def test_simulado_resposta_malformada(self, mock_post):
        """Simula API retornando JSON sem o campo 'choices'."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}  # Formato sem choices
        mock_post.return_value = mock_response

        with self.assertRaises(LLMClientError) as contexto:
            self.classifier.classificar("Alerta de teste")
        self.assertIn("formato inesperado", str(contexto.exception))

    # 6. Teste Real: Execução contra o LLM Local (Qwen 2.5 no Node03)
    def test_real_chamada_llm_local(self):
        """Execução ponta a ponta real contra o endpoint local."""
        try:
            resultado = self.classifier.classificar("O servidor web parou de responder.")
            self.assertIn("Prioridade:", resultado)
            self.assertIn("Justificativa:", resultado)
        except LLMUnavailableError:
            self.skipTest("LLM local não está ativo no momento para teste real.")


if __name__ == "__main__":
    unittest.main()