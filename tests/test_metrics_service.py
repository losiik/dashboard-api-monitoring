import os
import unittest
import uuid
from unittest.mock import Mock, patch

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_MAIN_DATABASE", "monitoring")
os.environ.setdefault("DB_USER", "postgres")
os.environ.setdefault("DB_PASSWORD", "postgres")
os.environ.setdefault("DADATA_API_KEY", "test-token")

from app.metrics_service import save_metric


class SaveMetricTests(unittest.TestCase):
    @patch("app.metrics_service.uuid.uuid4")
    @patch("app.metrics_service.ApiCheck")
    @patch("app.metrics_service.SessionLocal")
    def test_persists_metric_and_closes_session(self, session_local_mock, api_check_mock, uuid_mock):
        fake_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")
        session = Mock()
        record = Mock()
        metric = {
            "endpoint_type": "dadata_party_lookup",
            "status_code": 200,
            "response_time_ms": 82.5,
            "success": True,
            "error": None,
        }

        session_local_mock.return_value = session
        api_check_mock.return_value = record
        uuid_mock.return_value = fake_uuid

        save_metric(metric)

        api_check_mock.assert_called_once_with(
            id=fake_uuid,
            endpoint_type="dadata_party_lookup",
            status_code=200,
            response_time_ms=82.5,
            success=True,
            error=None,
        )
        session.add.assert_called_once_with(record)
        session.commit.assert_called_once_with()
        session.close.assert_called_once_with()

    @patch("app.metrics_service.ApiCheck")
    @patch("app.metrics_service.SessionLocal")
    def test_closes_session_even_when_commit_fails(self, session_local_mock, api_check_mock):
        session = Mock()
        session.commit.side_effect = RuntimeError("db unavailable")
        session_local_mock.return_value = session
        api_check_mock.return_value = Mock()

        with self.assertRaises(RuntimeError):
            save_metric(
                {
                    "endpoint_type": "dadata_party_lookup",
                    "status_code": 503,
                    "response_time_ms": 120.0,
                    "success": False,
                    "error": "dadata unavailable",
                }
            )

        session.close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
