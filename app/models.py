from datetime import datetime

from sqlalchemy import Column, Integer, Float, Boolean, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class ApiCheck(Base):
    __tablename__ = "api_check"

    id = Column(UUID, primary_key=True, index=True)
    endpoint_type = Column(String, index=True)
    status_code = Column(Integer)
    response_time_ms = Column(Float)
    success = Column(Boolean)
    error = Column(String, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow)
