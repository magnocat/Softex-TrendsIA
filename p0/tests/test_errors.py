"""
Bateria de Testes do P0 — Casos Reais e Simulados (Mocks)
Demonstração de resiliência e tratamento de falhas previsíveis (401, 409, 429, timeout e conexão).
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
    LLMRateLimitError,
    LLMConflictError,
    LLMClientError
)
from classifier import Classifier


class TestP0TratamentoDeErros(unittest.TestCase):

    def setUp(self):
        self.client = LLMClient()
        self.classifier = Classifier(self.client)

    def test_rejeicao_entrada_vazia(self):
        """Garante que entradas vazias ou espaços são impedidas antes de chamar o LLM."""
        with self.assertRaises(ValueError):
            self.classifier.classificar("   ")

    @patch("requests.post")
    def test_simulado_credencial_invalida_401(self, mock_post):
        """Simula resposta HTTP 401 para demonstrar tratamento de credencial inválida."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        with self.assertRaises(LLMAuthenticationError) as contexto:
            self.client.enviar_chat([{"role": "user", "content": "teste"}])
        self.assertIn("Credencial ausente ou inválida", str(contexto.exception))

    @patch("requests.post")
    def test_simulado_cota_excedida_429(self, mock_post):
        """Simula resposta HTTP 429 para demonstrar tratamento de estouro de cota / rate limit."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_post.return_value = mock_response

        with self.assertRaises(LLMRateLimitError) as contexto:
            self.client.enviar_chat([{"role": "user", "content": "teste"}])
        self.assertIn("Limite de cota ou taxa", str(contexto.exception))

    @patch("requests.post")
    def test_simulado_conflito_409(self, mock_post):
        """Simula resposta HTTP 409 para demonstrar tratamento de conflito de parâmetros."""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_post.return_value = mock_response

        with self.assertRaises(LLMConflictError) as contexto:
            self.client.enviar_chat([{"role": "user", "content": "teste"}])
        self.assertIn("Conflito de estado", str(contexto.exception))

    @patch("requests.post")
    def test_simulado_servico_indisponivel(self, mock_post):
        """Simula queda de rede ou serviço desligado."""
        mock_post.side_effect = requests.exceptions.ConnectionError("Conexão recusada")

        with self.assertRaises(LLMUnavailableError) as contexto:
            self.client.enviar_chat([{"role": "user", "content": "teste"}])
        self.assertIn("Falha de conexão", str(contexto.exception))

    @patch("requests.post")
    def test_simulado_timeout(self, mock_post):
        """Simula estouro do tempo limite configurado."""
        mock_post.side_effect = requests.exceptions.Timeout("Timeout atingido")

        with self.assertRaises(LLMTimeoutError) as contexto:
            self.client.enviar_chat([{"role": "user", "content": "teste"}])
        self.assertIn("Tempo limite", str(contexto.exception))

    @patch("requests.post")
    def test_simulado_resposta_malformada(self, mock_post):
        """Simula API retornando JSON sem o campo 'choices'."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}
        mock_post.return_value = mock_response

        with self.assertRaises(LLMClientError) as contexto:
            self.classifier.classificar("Alerta de teste")
        self.assertIn("formato inesperado", str(contexto.exception))

    def test_real_chamada_llm_local(self):
        """Execução ponta a ponta real contra o endpoint local."""
        try:
            resultado = self.classifier.classificar("O servidor web parou de responder.")
            self.assertIn("Prioridade:", resultado)
            self.assertIn("Justificativa:", resultado)
        except (LLMUnavailableError, LLMTimeoutError):
            self.skipTest("LLM local não respondeu a tempo ou está sobrecarregado no momento.")


if __name__ == "__main__":
    unittest.main()