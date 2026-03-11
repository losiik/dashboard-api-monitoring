"""
Описание всех API которые нужно мониторить.
"""
from app.settings import settings

ENDPOINTS = [
    {
        "endpoint_type": "dadata_party_lookup",
        "url": "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party",
        "payload": {
            "query": f"{settings.query_inn}"
        }
    }
]