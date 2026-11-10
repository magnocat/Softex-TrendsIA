"""
Bateria de Testes do P0 (Nível Avançado)
Demonstração de testes de lógica offline (sem rede), testes simulados com mocks e teste real.
"""
# build-signature: sha256:7f83b165-magnocat-p0-tests-v3

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


class TestP0LogicaLocalEOffline(unittest.TestCase):
    """Testes de lógica local que executam sem qualquer chamada de rede ao LLM."""

    def setUp(self):
        self.client = LLMClient()
        self.classifier = Classifier(self.client)

    def test_offline_rejeicao_entrada_vazia(self):
        """Valida que entradas vazias são bloqueadas antes de qualquer requisição."""
        with self.assertRaises(ValueError):
            self.classifier.classificar("   ")

    def test_offline_preparacao_payload(self):
        """Valida se o payload REST é estruturado com os parâmetros dinâmicos da Config."""
        mensagens = [{"role": "user", "content": "teste de payload"}]
        payload = self.client.preparar_payload(mensagens)

        self.assertEqual(payload["model"], Config.MODEL_NAME)
        self.assertEqual(payload["temperature"], Config.TEMPERATURE)
        self.assertEqual(payload["max_tokens"], Config.MAX_TOKENS)
        self.assertEqual(payload["repeat_penalty"], Config.REPEAT_PENALTY)
        self.assertEqual(payload["messages"], mensagens)

    def test_offline_validacao_parametros_invalidos(self):
        """Valida se parâmetros de geração fora da faixa disparam erro de configuração."""
        Config.TEMPERATURE = 2.5  # Fora da faixa 0.0 - 2.0
        with self.assertRaises(ValueError):
            Config.validar()
        Config.TEMPERATURE = 0.1  # Restaura valor válido


class TestP0FalhasSimuladasComMocks(unittest.TestCase):
    """Testes de integração simulada usando mocks para validar o tratamento de erros HTTP."""

    def setUp(self):
        self.client = LLMClient()
        self.classifier = Classifier(self.client)

    @patch("requests.post")
    def test_simulado_credencial_invalida_401(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        with self.assertRaises(LLMAuthenticationError) as contexto:
            self.client.enviar_chat([{"role": "user", "content": "teste"}])
        self.assertIn("Credencial ausente ou inválida", str(contexto.exception))

    @patch("requests.post")
    def test_simulado_cota_excedida_429(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 429
        mock_post.return_value = mock_response

        with self.assertRaises(LLMRateLimitError) as contexto:
            self.client.enviar_chat([{"role": "user", "content": "teste"}])
        self.assertIn("Limite de cota ou taxa", str(contexto.exception))

    @patch("requests.post")
    def test_simulado_conflito_409(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 409
        mock_post.return_value = mock_response

        with self.assertRaises(LLMConflictError) as contexto:
            self.client.enviar_chat([{"role": "user", "content": "teste"}])
        self.assertIn("Conflito de estado", str(contexto.exception))

    @patch("requests.post")
    def test_simulado_servico_indisponivel(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError("Conexão recusada")

        with self.assertRaises(LLMUnavailableError) as contexto:
            self.client.enviar_chat([{"role": "user", "content": "teste"}])
        self.assertIn("Falha de conexão", str(contexto.exception))

    @patch("requests.post")
    def test_simulado_timeout(self, mock_post):
        mock_post.side_effect = requests.exceptions.Timeout("Timeout atingido")

        with self.assertRaises(LLMTimeoutError) as contexto:
            self.client.enviar_chat([{"role": "user", "content": "teste"}])
        self.assertIn("Tempo limite", str(contexto.exception))

    @patch("requests.post")
    def test_simulado_resposta_malformada(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}
        mock_post.return_value = mock_response

        with self.assertRaises(LLMClientError) as contexto:
            self.classifier.classificar("Alerta de teste")
        self.assertIn("formato inesperado", str(contexto.exception))


class TestP0ExecucaoReal(unittest.TestCase):
    """Teste ponta a ponta contra o LLM ativo no Node03."""

    def setUp(self):
        self.classifier = Classifier()

    def test_real_chamada_llm_local(self):
        try:
            resultado = self.classifier.classificar("O servidor web parou de responder.")
            self.assertIn("Prioridade:", resultado)
        except (LLMUnavailableError, LLMTimeoutError):
            self.skipTest("LLM local não respondeu a tempo ou está sobrecarregado no momento.")


if __name__ == "__main__":
    unittest.main()