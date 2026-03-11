from app.db import SessionLocal
from app.models import ApiCheck
import uuid


def save_metric(metric):

    db = SessionLocal()

    try:
        record = ApiCheck(
            id=uuid.uuid4(),
            endpoint_type=metric["endpoint_type"],
            status_code=metric["status_code"],
            response_time_ms=metric["response_time_ms"],
            success=metric["success"],
            error=metric["error"]
        )

        db.add(record)
        db.commit()

    finally:
        db.close()
