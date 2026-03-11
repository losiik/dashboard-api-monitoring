import requests
import time

from app.settings import settings


def check_endpoint(endpoint):

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {settings.dadata_api_key}",
    }

    start = time.time()

    try:
        response = requests.post(
            endpoint["url"],
            json=endpoint["payload"],
            headers=headers,
            timeout=10
        )

        response_time = (time.time() - start) * 1000

        return {
            "endpoint_type": endpoint["endpoint_type"],
            "status_code": response.status_code,
            "response_time_ms": response_time,
            "success": response.status_code == 200,
            "error": None
        }

    except Exception as e:

        response_time = (time.time() - start) * 1000

        return {
            "endpoint_type": endpoint["endpoint_type"],
            "status_code": None,
            "response_time_ms": response_time,
            "success": False,
            "error": str(e)
        }
