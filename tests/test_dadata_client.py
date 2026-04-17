import os
import unittest
from unittest.mock import Mock, patch

import requests

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_MAIN_DATABASE", "monitoring")
os.environ.setdefault("DB_USER", "postgres")
os.environ.setdefault("DB_PASSWORD", "postgres")
os.environ.setdefault("DADATA_API_KEY", "test-token")

from app.dadata_client import check_endpoint


class CheckEndpointTests(unittest.TestCase):
    def setUp(self):
        self.endpoint = {
            "endpoint_type": "dadata_party_lookup",
            "url": "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party",
            "payload": {"query": "7707083893"},
        }

    @patch("app.dadata_client.time.time", side_effect=[100.0, 100.25])
    @patch("app.dadata_client.requests.post")
    def test_returns_success_metric_for_http_200(self, post_mock, _time_mock):
        response = Mock(status_code=200)
        post_mock.return_value = response

        metric = check_endpoint(self.endpoint)

        self.assertEqual(metric["endpoint_type"], self.endpoint["endpoint_type"])
        self.assertEqual(metric["status_code"], 200)
        self.assertAlmostEqual(metric["response_time_ms"], 250.0)
        self.assertTrue(metric["success"])
        self.assertIsNone(metric["error"])
        post_mock.assert_called_once_with(
            self.endpoint["url"],
            json=self.endpoint["payload"],
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Token test-token",
            },
            timeout=10,
        )

    @patch("app.dadata_client.time.time", side_effect=[200.0, 200.05])
    @patch("app.dadata_client.requests.post")
    def test_marks_metric_failed_when_dadata_returns_503(self, post_mock, _time_mock):
        post_mock.return_value = Mock(status_code=503)

        metric = check_endpoint(self.endpoint)

        self.assertEqual(metric["status_code"], 503)
        self.assertFalse(metric["success"])
        self.assertIsNone(metric["error"])
        self.assertAlmostEqual(metric["response_time_ms"], 50.0)

    @patch("app.dadata_client.time.time", side_effect=[300.0, 300.4])
    @patch("app.dadata_client.requests.post")
    def test_returns_error_metric_when_request_raises_timeout(self, post_mock, _time_mock):
        post_mock.side_effect = requests.exceptions.Timeout("dadata unavailable")

        metric = check_endpoint(self.endpoint)

        self.assertIsNone(metric["status_code"])
        self.assertFalse(metric["success"])
        self.assertAlmostEqual(metric["response_time_ms"], 400.0)
        self.assertIn("dadata unavailable", metric["error"])


if __name__ == "__main__":
    unittest.main()
