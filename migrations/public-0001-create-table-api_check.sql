CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE api_check (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    endpoint_type TEXT,
    status_code INTEGER,
    response_time_ms DOUBLE PRECISION,
    success BOOLEAN,
    error TEXT,
    checked_at TIMESTAMP DEFAULT NOW()
);