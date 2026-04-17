import os
import unittest
from unittest.mock import Mock, call, patch

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_MAIN_DATABASE", "monitoring")
os.environ.setdefault("DB_USER", "postgres")
os.environ.setdefault("DB_PASSWORD", "postgres")
os.environ.setdefault("DADATA_API_KEY", "test-token")

from app.scheduler import start_scheduler


class StartSchedulerTests(unittest.TestCase):
    @patch("builtins.print")
    @patch("app.scheduler.time.sleep")
    @patch("app.scheduler.save_metric")
    @patch("app.scheduler.check_endpoint")
    def test_checks_all_endpoints_and_sleeps_between_iterations(
        self,
        check_endpoint_mock,
        save_metric_mock,
        sleep_mock,
        _print_mock,
    ):
        endpoints = [
            {"endpoint_type": "party", "url": "https://dadata.test/party", "payload": {"query": "1"}},
            {"endpoint_type": "bank", "url": "https://dadata.test/bank", "payload": {"query": "2"}},
        ]
        metrics = [
            {"endpoint_type": "party", "success": True},
            {"endpoint_type": "bank", "success": False},
        ]

        check_endpoint_mock.side_effect = metrics
        sleep_mock.side_effect = RuntimeError("stop scheduler")

        with patch("app.scheduler.ENDPOINTS", endpoints), patch("app.scheduler.settings", Mock(check_interval=15)):
            with self.assertRaisesRegex(RuntimeError, "stop scheduler"):
                start_scheduler()

        self.assertEqual(check_endpoint_mock.call_args_list, [call(endpoints[0]), call(endpoints[1])])
        self.assertEqual(save_metric_mock.call_args_list, [call(metrics[0]), call(metrics[1])])
        sleep_mock.assert_called_once_with(15)


if __name__ == "__main__":
    unittest.main()
