import time

from app.settings import settings
from app.endpoints import ENDPOINTS
from app.dadata_client import check_endpoint
from app.metrics_service import save_metric


def start_scheduler():
    while True:
        for endpoint in ENDPOINTS:
            metric = check_endpoint(endpoint)
            save_metric(metric)
            print("checked:", metric)

        time.sleep(settings.check_interval)
